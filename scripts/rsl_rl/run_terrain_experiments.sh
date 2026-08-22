#!/usr/bin/env bash
set -u

PROJECT_DIR="/root/autodl-tmp/Isaaclab_Parkour"
RESULT_DIR="$PROJECT_DIR/results_terrain/full"
TEACHER_CHECKPOINT="$PROJECT_DIR/pretrained_official/2025-08-13_05-15-58/model_49999.pt"
STUDENT_CHECKPOINT="$PROJECT_DIR/pretrained_official/student_model_99998.pt"

export CONDA_PREFIX=/root/autodl-tmp/conda/envs/parkour
export PATH="$CONDA_PREFIX/bin:$PATH"
export LD_LIBRARY_PATH="$CONDA_PREFIX/lib:${LD_LIBRARY_PATH:-}"
export XDG_CACHE_HOME=/root/autodl-tmp/.cache

mkdir -p "$RESULT_DIR"
cd "$PROJECT_DIR"

variants=(
  hurdle_base hurdle_medium hurdle_hard
  step_base step_medium step_hard
  gap_base gap_medium gap_hard
  beam_base beam_medium beam_hard
)

run_policy() {
  local policy="$1"
  local task="$2"
  local checkpoint="$3"
  local variant json_path log_path

  for variant in "${variants[@]}"; do
    json_path="$RESULT_DIR/${policy}_${variant}.json"
    log_path="$RESULT_DIR/${policy}_${variant}.log"

    if [[ -s "$json_path" ]]; then
      printf '%s SKIP %s %s\n' "$(date --iso-8601=seconds)" "$policy" "$variant" | tee -a "$RESULT_DIR/status.log"
      continue
    fi

    printf '%s START %s %s\n' "$(date --iso-8601=seconds)" "$policy" "$variant" | tee -a "$RESULT_DIR/status.log"
    python -u scripts/rsl_rl/evaluation.py \
      --task "$task" \
      --headless \
      --checkpoint "$checkpoint" \
      --terrain_experiment "$variant" \
      --seed 42 \
      --evaluation_steps 1500 \
      --metrics_json "$json_path" \
      > "$log_path" 2>&1

    if [[ ! -s "$json_path" ]]; then
      printf '%s FAILED %s %s\n' "$(date --iso-8601=seconds)" "$policy" "$variant" | tee -a "$RESULT_DIR/status.log"
      tail -n 80 "$log_path"
      return 1
    fi
    printf '%s DONE %s %s\n' "$(date --iso-8601=seconds)" "$policy" "$variant" | tee -a "$RESULT_DIR/status.log"
  done
}

run_policy \
  teacher \
  Isaac-Extreme-Parkour-Teacher-Unitree-Go2-Eval-v0 \
  "$TEACHER_CHECKPOINT" || exit 1

run_policy \
  student \
  Isaac-Extreme-Parkour-Student-Unitree-Go2-Eval-v0 \
  "$STUDENT_CHECKPOINT" || exit 1

printf '%s ALL_DONE\n' "$(date --iso-8601=seconds)" | tee -a "$RESULT_DIR/status.log"
