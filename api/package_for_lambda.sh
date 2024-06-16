# Exit if any command failed
set -eux pipefail

pip install -t lib -r requirements.txt
(cd lib; zip ../lambda_function.zip -r .)
zip lambda_function.zip -u todo.py

# Clean up
rm -rf lib