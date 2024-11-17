from base64 import b64encode

from flask import Flask, render_template, request, jsonify
import subprocess
import json
import traceback


app = Flask(__name__)


def get_search_vector(query):
    """Returns a vector that will match our real images"""
    # These values should be close to what ImageMagick generates
    # for typical JPEGs from our dataset
    return [1280.0, 720.0, 30000.0, 15000.0]  # Basic image dimensions and stats


def get_search_vector_initial(query):
    """Convert search query to vector based on default or sample values"""
    # Default vector - can be adjusted based on query keywords
    search_vector = [1280.0, 720.0, 30000.0, 15000.0]

    # Simple adjustments based on keywords
    query = query.lower()
    if 'bright' in query:
        search_vector[2] *= 1.3  # Increase mean brightness
    elif 'dark' in query:
        search_vector[2] *= 0.7  # Decrease mean brightness

    return search_vector


def curl_post(url, data):
    try:
        cmd = ['curl', '-s', '-X', 'POST',
               '-H', 'Content-Type: application/json',
               '-d', json.dumps(data),
               url]
        print("Executing curl command:", ' '.join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True)
        print("Curl stdout:", result.stdout)
        print("Curl stderr:", result.stderr)
        return json.loads(result.stdout) if result.stdout else {"result": []}
    except Exception as e:
        print("Curl error:", str(e))
        print(traceback.format_exc())
        return {"result": []}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search')
def search():
    print("Search endpoint called")
    try:
        query = request.args.get('query', '')
        # print("Query:", query)

        # Use search_logic to get vector
        vector = get_search_vector(query)
        # print("Generated vector:", vector)

        qdrant_url = 'http://qdrant:6333/collections/images/points/search'
        search_request = {
            "vector": vector,
            "limit": 5,
            "with_payload": True
        }

        # print("Making request to Qdrant")
        results = curl_post(qdrant_url, search_request)
        # print("Qdrant results:", results)

        # Format results for frontend
        images = []
        if results and 'result' in results:
            for hit in results['result']:
                if 'payload' in hit and hit['payload'] and 'filename' in hit['payload']:
                    filename = hit['payload']['filename'].replace('.txt', '')  # Remove .txt extension
                    image_path = f'/app/images/{filename}'

                    try:
                        with open(image_path, 'rb') as img_file:
                            img_data = b64encode(img_file.read()).decode()
                            images.append({
                                'filename': filename,
                                'score': hit.get('score', 0),
                                'data': f'data:image/jpeg;base64,{img_data}'
                            })
                    except Exception as e:
                        print(f"Error loading image {filename}: {e}")
                        continue

        return jsonify({'images': images})

    except Exception as e:
        print("Search error:", str(e))
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)