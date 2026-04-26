# ------------------------------------------------------------
# Instagram Profile Info API - Nexxon Hackers Edition
# Developed by: Creator Shyamchand & Ayan
# Organization: CEO & Founder Of - Nexxon Hackers
# 100% FREE - No API Keys Required
# ------------------------------------------------------------

from flask import Flask, request, jsonify, render_template_string
import requests
from collections import OrderedDict
import re
import json
from datetime import datetime
import time
from functools import lru_cache

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# ---------------- CONFIG ----------------
COPYRIGHT_STRING = "Creator Shyamchand & Ayan - CEO & Founder Of - Nexxon Hackers"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "x-ig-app-id": "936619743392459",
    "Referer": "https://www.instagram.com/"
}

DESIRED_ORDER = [
    "username", "full_name", "id", "biography", "is_private",
    "is_verified", "profile_pic_url", "followers_count",
    "following_count", "media_count", "recent_posts",
    "checked_at"
]

# ---------------- HTML TEMPLATE ----------------
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Instagram Profile API - Nexxon Hackers</title>
<script src="https://cdn.tailwindcss.com/3.4.16"></script>
<link href="https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.6.0/remixicon.min.css" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-java.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js"></script>
<script>tailwind.config={theme:{extend:{colors:{primary:'#E1306C',secondary:'#C13584',tertiary:'#833AB4'}}}}</script>
<style>
:root { --primary: #E1306C; --secondary: #C13584; }
.insta-gradient { background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); }
.endpoint-card { transition: all 0.3s ease; border-left: 4px solid var(--primary); }
.endpoint-card:hover { transform: translateX(4px); box-shadow: 0 20px 25px -5px rgba(225,48,108,0.2); }
.code-block { max-height: 400px; overflow-y: auto; }
pre { margin: 0 !important; border-radius: 8px !important; }
.tab-btn { transition: all 0.2s; cursor: pointer; }
.tab-btn.active { background: #E1306C !important; color: white !important; }
.json-viewer { background: #1e1e1e; border-radius: 8px; padding: 16px; overflow-x: auto; font-family: 'Monaco',monospace; font-size: 13px; max-height: 500px; }
.json-key { color: #9cdcfe; } .json-string { color: #ce9178; } .json-number { color: #b5cea8; }
</style>
</head>
<body class="bg-gradient-to-br from-pink-50 via-white to-purple-50 min-h-screen">
<main class="pt-4 md:pt-8 pb-8 md:pb-12 px-3 md:px-4 max-w-7xl mx-auto">
    
    <header class="text-center py-6 md:py-10">
        <div class="inline-flex items-center justify-center w-16 h-16 md:w-24 md:h-24 insta-gradient rounded-2xl md:rounded-3xl mb-4 md:mb-6 shadow-xl">
            <i class="ri-instagram-line text-white text-2xl md:text-4xl"></i>
        </div>
        <h1 class="text-3xl md:text-5xl font-extrabold text-gray-900 mb-2">Instagram Profile API</h1>
        <p class="text-base md:text-xl text-gray-600 mb-2">Free Instagram Public Profile Data</p>
        <p class="text-xs text-gray-500">No Login • No API Key • Public Data Only</p>
        <div class="mt-3 inline-flex flex-wrap justify-center gap-1 md:gap-2">
            <span class="px-2 md:px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">100% Free</span>
            <span class="px-2 md:px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-xs font-medium">No API Key</span>
            <span class="px-2 md:px-3 py-1 bg-pink-100 text-pink-700 rounded-full text-xs font-medium">Real Data</span>
        </div>
    </header>

    <!-- Live Test -->
    <section class="mb-8 bg-white rounded-3xl p-4 md:p-8 shadow-xl border border-pink-100">
        <h2 class="text-lg md:text-2xl font-bold text-gray-900 mb-4">🔍 Live API Test</h2>
        
        <div class="flex flex-col sm:flex-row gap-3 mb-4">
            <input type="text" id="usernameInput" placeholder="Enter Instagram username (e.g., instagram)" 
                   class="flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-pink-500 outline-none text-sm"
                   value="instagram"
                   oninput="this.value = this.value.replace('@', '')">
            <button id="searchBtn" class="insta-gradient text-white px-6 py-3 rounded-xl font-semibold hover:shadow-xl transition flex items-center justify-center gap-2 text-sm">
                <i class="ri-search-line"></i>
                <span>Get Profile</span>
            </button>
        </div>
        
        <div class="flex gap-2 mb-4 flex-wrap">
            <span class="text-xs text-gray-500 py-1">Quick:</span>
            <button onclick="document.getElementById('usernameInput').value='instagram'; document.getElementById('searchBtn').click()" class="text-xs bg-pink-50 hover:bg-pink-100 px-3 py-1.5 rounded-full text-pink-700 transition border border-pink-200">@instagram</button>
            <button onclick="document.getElementById('usernameInput').value='cristiano'; document.getElementById('searchBtn').click()" class="text-xs bg-pink-50 hover:bg-pink-100 px-3 py-1.5 rounded-full text-pink-700 transition border border-pink-200">@cristiano</button>
            <button onclick="document.getElementById('usernameInput').value='leomessi'; document.getElementById('searchBtn').click()" class="text-xs bg-pink-50 hover:bg-pink-100 px-3 py-1.5 rounded-full text-pink-700 transition border border-pink-200">@leomessi</button>
            <button onclick="document.getElementById('usernameInput').value='virat.kohli'; document.getElementById('searchBtn').click()" class="text-xs bg-pink-50 hover:bg-pink-100 px-3 py-1.5 rounded-full text-pink-700 transition border border-pink-200">@virat.kohli</button>
        </div>
        
        <div id="responseContainer" class="hidden">
            <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-semibold text-gray-700">Response:</span>
                <button id="copyBtn" class="text-xs bg-pink-50 hover:bg-pink-100 text-pink-600 px-3 py-1.5 rounded-lg transition flex items-center gap-1">
                    <i class="ri-file-copy-line"></i> Copy JSON
                </button>
            </div>
            <pre id="responseDisplay" class="json-viewer"></pre>
        </div>
        
        <div id="loadingContainer" class="hidden text-center py-8">
            <div class="inline-block w-10 h-10 border-4 border-pink-200 border-t-pink-600 rounded-full animate-spin"></div>
            <p class="mt-3 text-gray-500">Fetching profile...</p>
        </div>
        
        <div id="errorContainer" class="hidden bg-red-50 border-2 border-red-200 rounded-xl p-4 text-red-700 mt-3">
            <p id="errorText"></p>
        </div>
    </section>

    <!-- Documentation -->
    <section class="mb-8">
        <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-4 text-center">📡 API Documentation</h2>
        
        <div class="bg-white rounded-2xl p-4 md:p-6 shadow-lg mb-4 endpoint-card">
            <div class="flex items-center justify-between mb-4">
                <div class="flex items-center gap-3">
                    <span class="w-10 h-10 insta-gradient rounded-xl flex items-center justify-center text-white text-lg">👤</span>
                    <div>
                        <h3 class="text-lg md:text-xl font-bold text-gray-900">Get Profile</h3>
                        <p class="text-xs text-gray-500">Fetch Instagram profile data</p>
                    </div>
                </div>
                <span class="px-3 py-1.5 bg-green-100 text-green-700 text-xs font-bold rounded-full">GET</span>
            </div>
            
            <div class="bg-gray-900 rounded-lg p-3 mb-3">
                <code class="text-green-400 text-sm">/api/profile/{username}</code>
            </div>
            
            <div class="mt-4 border-t pt-4">
                <p class="text-sm font-semibold mb-3">💻 Code Examples:</p>
                <div class="flex gap-1 mb-3 flex-wrap">
                    <button onclick="showCode(this, 'code-python')" class="tab-btn active px-3 py-1.5 text-xs rounded-lg bg-gray-200 font-medium">🐍 Python</button>
                    <button onclick="showCode(this, 'code-java')" class="tab-btn px-3 py-1.5 text-xs rounded-lg bg-gray-200 font-medium">☕ Java</button>
                    <button onclick="showCode(this, 'code-js')" class="tab-btn px-3 py-1.5 text-xs rounded-lg bg-gray-200 font-medium">📜 JavaScript</button>
                    <button onclick="showCode(this, 'code-curl')" class="tab-btn px-3 py-1.5 text-xs rounded-lg bg-gray-200 font-medium">📟 cURL</button>
                </div>
                
                <div id="code-python" class="code-block">
                    <pre class="language-python"><code>import requests

username = "instagram"
url = f"https://api.example.com/api/profile/{username}"

response = requests.get(url)
data = response.json()

if data.get("success"):
    print(f"👤 Name: {data['full_name']}")
    print(f"📝 Bio: {data['biography']}")
    print(f"👥 Followers: {data['followers_count']}")
    print(f"📸 Posts: {data['media_count']}")
    print(f"✅ Verified: {data['is_verified']}")
    print(f"🔒 Private: {data['is_private']}")
else:
    print(f"❌ Error: {data.get('error')}")</code></pre>
                </div>
                
                <div id="code-java" class="code-block hidden">
                    <pre class="language-java"><code>// Using OkHttp
OkHttpClient client = new OkHttpClient();
Request request = new Request.Builder()
    .url("https://api.example.com/api/profile/instagram")
    .build();

try (Response response = client.newCall(request).execute()) {
    String jsonData = response.body().string();
    System.out.println(jsonData);
}</code></pre>
                </div>
                
                <div id="code-js" class="code-block hidden">
                    <pre class="language-javascript"><code>const username = "instagram";
fetch(`https://api.example.com/api/profile/${username}`)
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      console.log(`${data.full_name} - ${data.followers_count} followers`);
    }
  });</code></pre>
                </div>
                
                <div id="code-curl" class="code-block hidden">
                    <pre class="language-bash"><code>curl "https://api.example.com/api/profile/instagram"</code></pre>
                </div>
            </div>
        </div>
        
        <!-- Sample Response -->
        <div class="bg-gray-900 rounded-2xl p-4 md:p-6">
            <h3 class="text-lg md:text-xl font-bold text-white mb-4">📋 Sample Response</h3>
            <pre class="text-green-400 text-xs overflow-x-auto">{
  "success": true,
  "username": "instagram",
  "full_name": "Instagram",
  "id": "25025320",
  "biography": "Bringing you closer to people...",
  "is_private": false,
  "is_verified": true,
  "profile_pic_url": "https://...",
  "followers_count": 678000000,
  "following_count": 120,
  "media_count": 7823,
  "recent_posts": [...],
  "checked_at": "2026-04-26 10:30:45 UTC",
  "api_info": {
    "developed_by": "Creator Shyamchand & Ayan",
    "organization": "CEO & Founder Of - Nexxon Hackers"
  }
}</pre>
        </div>
    </section>

    <div class="text-center py-6">
        <div class="inline-block insta-gradient text-white px-6 md:px-10 py-4 md:py-5 rounded-2xl md:rounded-3xl shadow-xl">
            <p class="font-bold text-lg md:text-2xl">Developed by Creator Shyamchand & Ayan</p>
            <p class="text-sm md:text-lg opacity-95">CEO & Founder Of - Nexxon Hackers</p>
        </div>
    </div>

</main>

<script>
function showCode(btn, id) {
    const parent = btn.parentElement.parentElement;
    parent.querySelectorAll('.code-block').forEach(b => b.classList.add('hidden'));
    parent.querySelectorAll('.tab-btn').forEach(b => {
        b.classList.remove('active', '!bg-pink-600', 'text-white');
        b.classList.add('bg-gray-200');
    });
    document.getElementById(id).classList.remove('hidden');
    btn.classList.add('active', '!bg-pink-600', 'text-white');
}
document.querySelectorAll('.tab-btn.active').forEach(btn => {
    btn.classList.add('!bg-pink-600', 'text-white');
});

function syntaxHighlight(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\\s*:)?|\\b(true|false|null)\\b|-?\\d+(?:\\.\\d*)?(?:[eE][+\\-]?\\d+)?)/g, function(m) {
        let cls = 'json-number';
        if (/^"/.test(m)) cls = m.includes(':') ? 'json-key' : 'json-string';
        else if (/true|false/.test(m)) cls = 'json-boolean';
        else if (/null/.test(m)) cls = 'json-null';
        return '<span class="' + cls + '">' + m + '</span>';
    });
}

async function fetchProfile() {
    const username = document.getElementById('usernameInput').value.trim().replace('@', '');
    if (!username) { alert('Please enter a username'); return; }
    
    document.getElementById('responseContainer').classList.add('hidden');
    document.getElementById('errorContainer').classList.add('hidden');
    document.getElementById('loadingContainer').classList.remove('hidden');
    
    try {
        const response = await fetch('/api/profile/' + encodeURIComponent(username));
        const data = await response.json();
        
        document.getElementById('loadingContainer').classList.add('hidden');
        
        const jsonStr = JSON.stringify(data, null, 2);
        document.getElementById('responseDisplay').innerHTML = syntaxHighlight(jsonStr);
        document.getElementById('responseContainer').classList.remove('hidden');
        
    } catch (error) {
        document.getElementById('loadingContainer').classList.add('hidden');
        document.getElementById('errorText').textContent = error.message;
        document.getElementById('errorContainer').classList.remove('hidden');
    }
}

document.getElementById('searchBtn').addEventListener('click', fetchProfile);
document.getElementById('usernameInput').addEventListener('keypress', (e) => { if (e.key === 'Enter') fetchProfile(); });

document.getElementById('copyBtn').addEventListener('click', function() {
    const text = document.getElementById('responseDisplay').textContent;
    navigator.clipboard.writeText(text).then(() => {
        const btn = document.getElementById('copyBtn');
        btn.innerHTML = '<i class="ri-check-line"></i> Copied!';
        setTimeout(() => btn.innerHTML = '<i class="ri-file-copy-line"></i> Copy JSON', 2000);
    });
});
</script>
</body>
</html>
'''

# ---------------- INSTAGRAM SCRAPER ----------------
@lru_cache(maxsize=128)
def fetch_instagram_profile(username):
    """Fetch Instagram profile data - FREE method"""
    username = username.strip().replace('@', '')
    
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
    
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                user = data.get("data", {}).get("user") or data.get("user") or {}
                
                if not user:
                    return None
                
                result = OrderedDict()
                result["success"] = True
                result["username"] = user.get("username", username)
                result["full_name"] = user.get("full_name", "N/A")
                result["id"] = user.get("id", "N/A")
                result["biography"] = user.get("biography", "N/A")
                result["is_private"] = user.get("is_private", False)
                result["is_verified"] = user.get("is_verified", False)
                result["profile_pic_url"] = user.get("profile_pic_url_hd") or user.get("profile_pic_url", "N/A")
                result["followers_count"] = user.get("edge_followed_by", {}).get("count", 0) or user.get("followers_count", 0)
                result["following_count"] = user.get("edge_follow", {}).get("count", 0) or user.get("following_count", 0)
                result["media_count"] = user.get("edge_owner_to_timeline_media", {}).get("count", 0) or user.get("media_count", 0)
                
                # Recent posts
                media = user.get("edge_owner_to_timeline_media", {})
                edges = media.get("edges", [])[:6]
                recent = []
                for edge in edges:
                    node = edge.get("node", {})
                    if node:
                        recent.append({
                            "id": node.get("id"),
                            "shortcode": node.get("shortcode"),
                            "display_url": node.get("display_url"),
                            "likes": node.get("edge_liked_by", {}).get("count", 0),
                            "caption": node.get("edge_media_to_caption", {}).get("edges", [{}])[0].get("node", {}).get("text", "") if node.get("edge_media_to_caption") else ""
                        })
                result["recent_posts"] = recent
                result["checked_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
                result["api_info"] = {
                    "developed_by": "Creator Shyamchand & Ayan",
                    "organization": "CEO & Founder Of - Nexxon Hackers",
                    "version": "1.0.0"
                }
                
                return result
                
            elif resp.status_code == 404:
                return {"success": False, "error": "User not found", "username": username}
            else:
                time.sleep(1)
                
        except Exception as e:
            time.sleep(1)
    
    return {"success": False, "error": "Failed to fetch profile. Try again later.", "username": username}

# ---------------- API ROUTES ----------------
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/profile/<username>")
def api_profile(username):
    result = fetch_instagram_profile(username)
    
    if result is None:
        return jsonify({
            "success": False,
            "error": "User not found or private account",
            "api_info": {
                "developed_by": "Creator Shyamchand & Ayan",
                "organization": "CEO & Founder Of - Nexxon Hackers"
            }
        }), 404
    
    return app.response_class(
        response=json.dumps(result, ensure_ascii=False, indent=2),
        mimetype='application/json'
    )

@app.route("/api/batch", methods=["POST"])
def api_batch():
    try:
        data = request.get_json()
        
        if not data or "usernames" not in data:
            return jsonify({
                "success": False,
                "error": "Please provide JSON with 'usernames' array"
            }), 400
        
        usernames = data["usernames"][:10]
        results = []
        
        for username in usernames:
            result = fetch_instagram_profile(username)
            results.append(result if result else {"success": False, "username": username})
        
        return jsonify({
            "success": True,
            "total": len(results),
            "results": results,
            "api_info": {
                "developed_by": "Creator Shyamchand & Ayan",
                "organization": "CEO & Founder Of - Nexxon Hackers"
            }
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "api_info": {
            "developed_by": "Creator Shyamchand & Ayan",
            "organization": "CEO & Founder Of - Nexxon Hackers"
        }
    }), 404

# ---------------- MAIN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
