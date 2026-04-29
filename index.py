# ------------------------------------------------------------
# Instagram Profile API - Nexxon Hackers Edition
# Developed by: Creator Shyamchand & Ayan
# Organization: CEO & Founder Of - Nexxon Hackers
# Features: JSON API + Beautiful Profile Viewer + IMGBB Image Proxy
# ------------------------------------------------------------

from flask import Flask, request, jsonify, render_template_string
import requests
from collections import OrderedDict
import re
import json
from datetime import datetime
import time
from functools import lru_cache
import base64

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# ---------------- CONFIG ----------------
COPYRIGHT_STRING = "Creator Shyamchand & Ayan - CEO & Founder Of - Nexxon Hackers"
IMGBB_API_KEY = "8fb0a4e7c707858edd73349d5cf4f6e14"
IMGBB_API_URL = "https://api.imgbb.com/1/upload"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "x-ig-app-id": "936619743392459",
    "Referer": "https://www.instagram.com/"
}

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
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-javascript.min.js"></script>
<style>
:root { --primary: #E1306C; }
.insta-gradient { background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); }
.endpoint-card { transition: all 0.3s ease; border-left: 4px solid var(--primary); }
.endpoint-card:hover { transform: translateX(4px); box-shadow: 0 20px 25px -5px rgba(225,48,108,0.2); }
.code-block { max-height: 400px; overflow-y: auto; }
pre { margin: 0 !important; border-radius: 8px !important; }
.tab-btn { transition: all 0.2s; cursor: pointer; }
.tab-btn.active { background: #E1306C !important; color: white !important; }
.json-viewer { background: #1e1e1e; border-radius: 8px; padding: 16px; overflow-x: auto; font-family: monospace; font-size: 13px; max-height: 500px; }
/* Instagram Profile Card - Dark Theme */
.ig-card {
    background: #181818;
    border-radius: 20px;
    padding: 24px;
    color: white;
    max-width: 420px;
    margin: 0 auto;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
    box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.ig-header { display: flex; align-items: center; gap: 14px; margin-bottom: 22px; }
.ig-avatar {
    width: 80px; height: 80px; border-radius: 50%;
    border: 2.5px solid #fff;
    object-fit: cover; background: #2a2a2a;
    flex-shrink: 0;
    box-shadow: 0 0 20px rgba(225,48,108,0.3);
}
.ig-avatar-placeholder {
    width: 80px; height: 80px; border-radius: 50%;
    background: linear-gradient(135deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; font-weight: bold; color: white; flex-shrink: 0;
}
.ig-username-badge {
    background: rgba(255,255,255,0.12);
    padding: 7px 16px; border-radius: 20px;
    font-size: 15px; font-weight: 600; letter-spacing: 0.3px;
}
.ig-stats { display: flex; justify-content: space-around; margin-bottom: 22px; text-align: center; }
.ig-stat-num { font-size: 19px; font-weight: 700; letter-spacing: 0.5px; }
.ig-stat-label { font-size: 13px; color: #aaa; margin-top: 3px; }
.ig-fullname { font-size: 15px; font-weight: 600; color: #fff; }
.ig-subtitle { font-size: 13px; color: #aaa; margin-top: 3px; }
.ig-divider { border-top: 1px solid #2a2a2a; margin: 12px 0; }
.ig-bio { font-size: 12.5px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; color: #ccc; line-height: 1.6; white-space: pre-line; }
.ig-badge { display: inline-block; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; margin-top: 8px; }
.ig-badge-verified { background: #3897f0; color: white; }
.ig-badge-private { background: #ff4757; color: white; }
.ig-posts-section { margin-top: 20px; }
.ig-posts-title { font-size: 13px; color: #888; margin-bottom: 12px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; }
.ig-posts-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
.ig-post {
    position: relative; border-radius: 10px; overflow: hidden;
    cursor: pointer; background: #1a1a1a;
    aspect-ratio: 1;
    transition: transform 0.2s;
}
.ig-post:hover { transform: scale(1.03); }
.ig-post img {
    width: 100%; height: 100%; object-fit: cover; display: block;
    transition: opacity 0.3s;
}
.ig-post-overlay {
    position: absolute; top: 6px; right: 6px;
    background: rgba(0,0,0,0.65);
    padding: 3px 8px; border-radius: 10px;
    color: white; font-size: 10px;
    display: flex; align-items: center; gap: 3px;
    backdrop-filter: blur(4px);
}
.ig-post-caption {
    position: absolute; bottom: 6px; left: 6px; right: 6px;
    background: rgba(0,0,0,0.55);
    padding: 3px 7px; border-radius: 6px;
    color: #ddd; font-size: 9.5px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    backdrop-filter: blur(4px);
}
.ig-post-loading {
    display: flex; align-items: center; justify-content: center;
    color: #666; font-size: 11px;
}
.tab-container { display: flex; gap: 2px; margin-bottom: 20px; background: #1a1a1a; border-radius: 12px; padding: 4px; }
.tab-option { flex: 1; text-align: center; padding: 10px; border-radius: 10px; cursor: pointer; font-size: 14px; font-weight: 600; transition: all 0.2s; color: #888; }
.tab-option.active { background: #333; color: white; }
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
        <p class="text-xs text-gray-500">No Login • No API Key • IMGBB Image Proxy</p>
        <div class="mt-3 inline-flex flex-wrap justify-center gap-1 md:gap-2">
            <span class="px-2 md:px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-medium">100% Free</span>
            <span class="px-2 md:px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-medium">IMGBB Proxy</span>
            <span class="px-2 md:px-3 py-1 bg-pink-100 text-pink-700 rounded-full text-xs font-medium">Real Data</span>
        </div>
    </header>

    <!-- Live Test -->
    <section class="mb-8 bg-white rounded-3xl p-4 md:p-8 shadow-xl border border-pink-100">
        <h2 class="text-lg md:text-2xl font-bold text-gray-900 mb-4">🔍 Live Profile Viewer</h2>
        
        <!-- Tab Switcher -->
        <div class="tab-container mb-4">
            <div id="tabProfile" class="tab-option active" onclick="switchView('profile')">
                <i class="ri-user-line mr-1"></i> Profile Card
            </div>
            <div id="tabJson" class="tab-option" onclick="switchView('json')">
                <i class="ri-braces-line mr-1"></i> JSON Response
            </div>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-3 mb-4">
            <input type="text" id="usernameInput" placeholder="Enter Instagram username (e.g., creator_shyamchand_07)" 
                   class="flex-1 px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-pink-500 outline-none text-sm"
                   value="creator_shyamchand_07"
                   oninput="this.value = this.value.replace('@', '')">
            <button id="searchBtn" class="insta-gradient text-white px-6 py-3 rounded-xl font-semibold hover:shadow-xl transition flex items-center justify-center gap-2 text-sm">
                <i class="ri-search-line"></i>
                <span>Get Profile</span>
            </button>
        </div>
        
        <div class="flex gap-2 mb-4 flex-wrap">
            <span class="text-xs text-gray-500 py-1">Quick:</span>
            <button onclick="document.getElementById('usernameInput').value='creator_shyamchand_07'; document.getElementById('searchBtn').click()" class="text-xs bg-pink-50 hover:bg-pink-100 px-3 py-1.5 rounded-full text-pink-700 transition border border-pink-200">@creator_shyamchand_07</button>
            <button onclick="document.getElementById('usernameInput').value='instagram'; document.getElementById('searchBtn').click()" class="text-xs bg-pink-50 hover:bg-pink-100 px-3 py-1.5 rounded-full text-pink-700 transition border border-pink-200">@instagram</button>
            <button onclick="document.getElementById('usernameInput').value='cristiano'; document.getElementById('searchBtn').click()" class="text-xs bg-pink-50 hover:bg-pink-100 px-3 py-1.5 rounded-full text-pink-700 transition border border-pink-200">@cristiano</button>
        </div>
        
        <!-- Profile Card View -->
        <div id="profileView" class="hidden">
            <div id="profileCard"></div>
        </div>
        
        <!-- JSON View -->
        <div id="jsonView" class="hidden">
            <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-semibold text-gray-700">JSON Response:</span>
                <button id="copyBtn" class="text-xs bg-pink-50 hover:bg-pink-100 text-pink-600 px-3 py-1.5 rounded-lg transition flex items-center gap-1">
                    <i class="ri-file-copy-line"></i> Copy JSON
                </button>
            </div>
            <pre id="jsonDisplay" class="json-viewer"></pre>
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
                        <p class="text-xs text-gray-500">Fetch Instagram profile data with IMGBB proxy images</p>
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
                    <button onclick="showCode(this, 'code-js')" class="tab-btn px-3 py-1.5 text-xs rounded-lg bg-gray-200 font-medium">📜 JavaScript</button>
                    <button onclick="showCode(this, 'code-curl')" class="tab-btn px-3 py-1.5 text-xs rounded-lg bg-gray-200 font-medium">📟 cURL</button>
                </div>
                
                <div id="code-python" class="code-block">
                    <pre class="language-python"><code>import requests

# Get profile with IMGBB proxy images
response = requests.get(
    "https://api.example.com/api/profile/creator_shyamchand_07"
)
data = response.json()

if data.get("success"):
    print(f"👤 {data['full_name']}")
    print(f"👥 {data['followers_count']} followers")
    print(f"🖼️ Avatar: {data['profile_pic_url']}")
    for post in data['recent_posts']:
        print(f"📸 {post['display_url']}")</code></pre>
                </div>
                
                <div id="code-js" class="code-block hidden">
                    <pre class="language-javascript"><code>fetch("https://api.example.com/api/profile/creator_shyamchand_07")
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      console.log(`${data.full_name} - ${data.followers_count} followers`);
      // All image URLs are IMGBB proxy links
      document.getElementById('avatar').src = data.profile_pic_url;
    }
  });</code></pre>
                </div>
                
                <div id="code-curl" class="code-block hidden">
                    <pre class="language-bash"><code>curl "https://api.example.com/api/profile/creator_shyamchand_07"</code></pre>
                </div>
            </div>
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
let currentView = 'profile';
let currentData = null;

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

function switchView(view) {
    currentView = view;
    document.getElementById('tabProfile').classList.toggle('active', view === 'profile');
    document.getElementById('tabJson').classList.toggle('active', view === 'json');
    document.getElementById('profileView').classList.toggle('hidden', view !== 'profile');
    document.getElementById('jsonView').classList.toggle('hidden', view !== 'json');
    if (currentData) displayData(currentData);
}

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

function formatNumber(num) {
    if (!num) return '0';
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
}

function buildProfileCard(data) {
    const posts = data.recent_posts || [];
    const postsHTML = posts.slice(0, 6).map(post => `
        <div class="ig-post" onclick="window.open('https://www.instagram.com/p/${post.shortcode}', '_blank')">
            <img src="${post.display_url}" alt="Post" 
                 onerror="this.parentElement.innerHTML='<div class=\\'ig-post-loading\\' style=\\'height:100%\\'>📷</div>'"
                 loading="lazy">
            ${post.likes ? `<div class="ig-post-overlay">❤️ ${formatNumber(post.likes)}</div>` : ''}
            ${post.caption ? `<div class="ig-post-caption">${post.caption.substring(0, 40)}</div>` : ''}
        </div>
    `).join('');

    // Check if avatar is valid
    const avatarHTML = data.profile_pic_url && data.profile_pic_url !== 'N/A'
        ? `<img src="${data.profile_pic_url}" alt="${data.username}" class="ig-avatar" onerror="this.style.display='none';this.nextElementSibling.style.display='flex';" loading="lazy">
           <div class="ig-avatar-placeholder" style="display:none">${(data.username || '?')[0].toUpperCase()}</div>`
        : `<div class="ig-avatar-placeholder">${(data.username || '?')[0].toUpperCase()}</div>`;

    return `
        <div class="ig-card">
            <div class="ig-header">
                ${avatarHTML}
                <div>
                    <div class="ig-username-badge">${data.username}</div>
                </div>
            </div>
            
            <div class="ig-stats">
                <div>
                    <div class="ig-stat-num">${formatNumber(data.media_count)}</div>
                    <div class="ig-stat-label">posts</div>
                </div>
                <div>
                    <div class="ig-stat-num">${formatNumber(data.followers_count)}</div>
                    <div class="ig-stat-label">followers</div>
                </div>
                <div>
                    <div class="ig-stat-num">${formatNumber(data.following_count)}</div>
                    <div class="ig-stat-label">following</div>
                </div>
            </div>
            
            <div class="ig-fullname">${data.full_name} ${data.is_verified ? '✅' : ''}</div>
            ${data.biography ? `<div class="ig-subtitle">${data.biography.split('\\n')[0]}</div>` : ''}
            <div class="ig-divider"></div>
            <div class="ig-bio">${data.biography ? data.biography.toUpperCase() : 'No bio'}</div>
            
            <div style="margin-top:8px;display:flex;gap:6px;">
                ${data.is_verified ? '<span class="ig-badge ig-badge-verified">✅ Verified</span>' : ''}
                ${data.is_private ? '<span class="ig-badge ig-badge-private">🔒 Private</span>' : ''}
            </div>
            
            ${posts.length > 0 ? `
            <div class="ig-posts-section">
                <div class="ig-posts-title">📸 Recent Posts</div>
                <div class="ig-posts-grid">${postsHTML}</div>
            </div>` : ''}
        </div>
    `;
}

function displayData(data) {
    currentData = data;
    if (currentView === 'profile') {
        document.getElementById('profileCard').innerHTML = buildProfileCard(data);
    } else {
        document.getElementById('jsonDisplay').innerHTML = syntaxHighlight(JSON.stringify(data, null, 2));
    }
}

async function fetchProfile() {
    const username = document.getElementById('usernameInput').value.trim().replace('@', '');
    if (!username) { alert('Please enter a username'); return; }
    
    document.getElementById('profileView').classList.add('hidden');
    document.getElementById('jsonView').classList.add('hidden');
    document.getElementById('errorContainer').classList.add('hidden');
    document.getElementById('loadingContainer').classList.remove('hidden');
    
    try {
        const response = await fetch('/api/profile/' + encodeURIComponent(username));
        const data = await response.json();
        
        document.getElementById('loadingContainer').classList.add('hidden');
        
        if (data.success) {
            displayData(data);
            document.getElementById(currentView === 'profile' ? 'profileView' : 'jsonView').classList.remove('hidden');
        } else {
            document.getElementById('errorText').textContent = data.error || 'Profile not found';
            document.getElementById('errorContainer').classList.remove('hidden');
        }
    } catch (error) {
        document.getElementById('loadingContainer').classList.add('hidden');
        document.getElementById('errorText').textContent = error.message;
        document.getElementById('errorContainer').classList.remove('hidden');
    }
}

document.getElementById('searchBtn').addEventListener('click', fetchProfile);
document.getElementById('usernameInput').addEventListener('keypress', (e) => { if (e.key === 'Enter') fetchProfile(); });
document.getElementById('copyBtn').addEventListener('click', () => {
    navigator.clipboard.writeText(document.getElementById('jsonDisplay').textContent);
    const btn = document.getElementById('copyBtn');
    btn.innerHTML = '<i class="ri-check-line"></i> Copied!';
    setTimeout(() => btn.innerHTML = '<i class="ri-file-copy-line"></i> Copy JSON', 2000);
});

// Auto-load default
window.addEventListener('load', () => {
    fetchProfile();
});
</script>
</body>
</html>
'''

# ---------------- IMGBB IMAGE UPLOAD ----------------
def upload_to_imgbb(image_url):
    """Upload image to IMGBB and return the viewer link"""
    try:
        # Fetch image from Instagram
        resp = requests.get(image_url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return image_url  # Fallback to original
        
        # Convert to base64 for IMGBB
        image_b64 = base64.b64encode(resp.content).decode('utf-8')
        
        # Upload to IMGBB
        payload = {
            'key': IMGBB_API_KEY,
            'image': image_b64,
        }
        
        upload_resp = requests.post(IMGBB_API_URL, data=payload, timeout=15)
        if upload_resp.status_code == 200:
            result = upload_resp.json()
            if result.get('success'):
                return result['data']['url']  # Return IMGBB viewer link
        
        return image_url  # Fallback to original
        
    except Exception as e:
        print(f"IMGBB upload error: {e}")
        return image_url  # Fallback to original

# ---------------- INSTAGRAM SCRAPER ----------------
@lru_cache(maxsize=128)
def fetch_instagram_profile(username):
    """Fetch Instagram profile data with IMGBB proxy images"""
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
                
                # Upload profile pic to IMGBB
                original_pic = user.get("profile_pic_url_hd") or user.get("profile_pic_url", "")
                result["profile_pic_url"] = upload_to_imgbb(original_pic) if original_pic else "N/A"
                
                result["followers_count"] = user.get("edge_followed_by", {}).get("count", 0) or user.get("followers_count", 0)
                result["following_count"] = user.get("edge_follow", {}).get("count", 0) or user.get("following_count", 0)
                result["media_count"] = user.get("edge_owner_to_timeline_media", {}).get("count", 0) or user.get("media_count", 0)
                
                # Recent posts with IMGBB proxy
                media = user.get("edge_owner_to_timeline_media", {})
                edges = media.get("edges", [])[:6]
                recent = []
                for edge in edges:
                    node = edge.get("node", {})
                    if node:
                        original_display = node.get("display_url", "")
                        imgbb_url = upload_to_imgbb(original_display) if original_display else ""
                        
                        like_count = 0
                        if node.get("edge_liked_by"):
                            like_count = node["edge_liked_by"].get("count", 0)
                        elif node.get("edge_media_preview_like"):
                            like_count = node["edge_media_preview_like"].get("count", 0)
                        
                        recent.append({
                            "id": node.get("id"),
                            "shortcode": node.get("shortcode"),
                            "display_url": imgbb_url or original_display,
                            "likes": like_count,
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
    
    return {"success": False, "error": "Failed to fetch profile", "username": username}

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
            return jsonify({"success": False, "error": "Please provide JSON with 'usernames' array"}), 400
        
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
