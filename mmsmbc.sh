#!/bin/bash

brpath="/media/fat/Scripts/.barcoderattler"

function curl_download() { # curl_download ${filepath} ${URL}
                curl \
                        --connect-timeout 15 --max-time 600 --retry 3 --retry-delay 5 --silent --show-error \
                        --insecure \
                        --fail \
                        --location \
                        -o "${1}" \
                        "${2}"
}

if [ ! -f "${brpath}/mbc" ]; then
   echo "Downloading MBC..."
   REPOSITORY_URL="https://github.com/mrchrisster/MiSTer_Batch_Control"
   mbcurl="blob/master/mbc_v06"

   curl_download "/tmp/mbc" "${REPOSITORY_URL}/${mbcurl}?raw=true"
   mkdir -p "${brpath}"
   mv --force "/tmp/mbc" "${brpath}/mbc"
fi
