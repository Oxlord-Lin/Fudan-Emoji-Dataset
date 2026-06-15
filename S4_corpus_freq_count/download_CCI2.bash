export HF_HUB_ENABLE_HF_TRANSFER=1


hf download BAAI/CCI2-Data \
  --repo-type dataset \
  --include "*.parquet" \
  --local-dir ./cci2_parquet