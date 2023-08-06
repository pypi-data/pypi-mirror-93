#!/bin/bash

# Install vendored packages into /tmp and then compare with what's in
# bleach/_vendor/.

DEST=/tmp/vendor-test

if [[ -e "${DEST}" ]]; then
    echo "${DEST} exists. Please remove."
    exit 1
fi

mkdir "${DEST}"

# Get versions of pip and python
pip --version

# Install vendored dependencies into temp directory
pip install --no-binary all --no-compile --no-deps -r bleach/_vendor/vendor.txt --target "${DEST}"

# Diff contents of temp directory and bleach/_vendor/ excluding vendoring
# infrastructure
echo "diffing directory trees..."
diff -r \
    --exclude="__init__.py" \
    --exclude="README.rst" \
    --exclude="vendor.txt" \
    --exclude="pip_install_vendor.sh" \
    --exclude="__pycache__" \
    --exclude="RECORD" \
    bleach/_vendor/ "${DEST}"

# Go through all RECORD files and compare sorted versions; RECORD files are
# unsorted and occasionally diff poorly
for fn in $(cd bleach/_vendor/; find . -name RECORD); do
    echo "diffing bleach/_vendor/${fn} and ${DEST}/${fn} ..."
    diff <(sort bleach/_vendor/${fn}) <(sort ${DEST}/${fn})
done

# If everything is cool, then delete the temp directory
LASTEXIT=$?
if [ ${LASTEXIT} -eq 0 ]; then
    rm -rf "${DEST}"
fi

exit ${LASTEXIT}
