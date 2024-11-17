#!/bin/sh

mkdir -p images

while IFS= read -r url; do
    echo "Downloading: $url"
    # Download to a temporary file first
    temp_file="temp_$(date +%s).jpg"
    curl -L "$url" -o "$temp_file"

    # Check if the file is a valid JPEG using 'file' command
    if file "$temp_file" | grep -iE "JPEG|PNG"; then
        # If it's a valid image, move it to final destination
        mv "$temp_file" "images/image_$(date +%s).jpg"
        echo "Successfully downloaded and verified image"
    else
        echo "Downloaded file is not a valid image, skipping: $url"
        rm "$temp_file"
    fi

    sleep 1
done < image_urls.txt
touch /app/images/.download_complete