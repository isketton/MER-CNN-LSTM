    echo "Please Enter the MP3Path -> "
    read mpath
    cd ${mpath}
    mkdir 'wav'

    for ((m=1; m<=1000; m++))
    do
    echo "Processing file: ${m}"
    ffmpeg -i "${m}.mp3" "wav/${m%.mp3}.wav"
    done