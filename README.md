<h1>ImageGenToolKit</h1>

<p><strong>ImageGenToolKit</strong> is a Python library for asynchronous AI image generation with built-in proxy support. This library uses the MagicHour AI platform and handles proxies automatically, making it ideal for generating images in environments with restricted or rate-limited access.</p>

<h2>Features</h2>
<ul>
  <li><strong>Asynchronous:</strong> Fully async operations for speed and scalability.</li>
  <li><strong>Proxy Support:</strong> Automatically fetches and rotates HTTP proxies.</li>
  <li><strong>Customizable:</strong> Allows prompt-based image generation with configurable orientation.</li>
</ul>

---

<h2>Installation</h2>

<p>Install the library using <code>pip</code>:</p>

<pre><code>pip install ImageGenToolKit
</code></pre>

---

<h2>Usage</h2>

<p>Here’s how to use the library to generate AI-generated images.</p>

<h3><strong>Basic Example</strong></h3>
<pre><code>import asyncio
from ImageGenToolKit import AIImageGeneratorAsync

async def main():
    # Initialize the image generator
    gen = AIImageGeneratorAsync()
    
    # Generate an image
    prompt = "A futuristic cityscape with glowing neon lights"
    urls = await gen.generate_image(prompt, orientation="landscape")
    
    # Print the image URLs
    print("Generated Image URLs:", urls)

# Run the async function
asyncio.run(main())
</code></pre>

<h3><strong>Output Example</strong></h3>
<pre><code>Generated Image URLs: [
    "https://example.com/image1.png",
    "https://example.com/image2.png"
]
</code></pre>

<h3><strong>Customizing Orientation</strong></h3>
<p>You can specify the orientation as <code>"portrait"</code>, <code>"landscape"</code>, or <code>"square"</code>:</p>
<pre><code>urls = await gen.generate_image("A serene mountain lake", orientation="portrait")
</code></pre>

---

<h2>Advanced Features</h2>

<h3><strong>Handling Proxies</strong></h3>
<p>The library automatically fetches and uses proxies. You can also fetch proxies manually if needed:</p>
<pre><code>await gen.fetch_proxies()
print(gen.proxy_list)  # List of fetched proxies
</code></pre>

<h3><strong>Error Handling</strong></h3>
<p>Make sure to handle exceptions in case of network issues or invalid proxies:</p>
<pre><code>try:
    urls = await gen.generate_image("A fantasy dragon in flight")
    print(urls)
except Exception as e:
    print("Error generating image:", e)
</code></pre>

---

<h2>Contributing</h2>
<ol>
  <li>Fork the repository.</li>
  <li>Create a feature branch: <code>git checkout -b feature-name</code>.</li>
  <li>Commit your changes: <code>git commit -m "Add new feature"</code>.</li>
  <li>Push to the branch: <code>git push origin feature-name</code>.</li>
  <li>Submit a pull request.</li>
</ol>

---

<h2>License</h2>

<p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</p>

---
