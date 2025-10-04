<script lang="ts">
  import { Link } from 'svelte-routing';
  import Footer from '../lib/components/layout/Footer.svelte';
  import CustomSelect from '../lib/components/CustomSelect.svelte';
  
  let algorithm = 'HS256';
  let secretKey = 'your-256-bit-secret';
  let publicKey = '';
  let privateKey = '';
  let generatedKeyPair: CryptoKeyPair | null = null;
  let keyGenerationStatus = '';
  
  let headerInput = JSON.stringify({ alg: "HS256", typ: "JWT" }, null, 2);
  let payloadInput = JSON.stringify({
    sub: "1234567890",
    name: "Dilroop Ummar Shameem",
    role: "Fullstack Engineer (Backend Focused)",
    iat: Math.floor(Date.now() / 1000)
  }, null, 2);
  
  let encodedToken = '';
  let decodedHeader = '';
  let decodedPayload = '';
  let verificationStatus = '';
  
  function base64urlEncode(str: string): string {
    return btoa(str)
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=/g, '');
  }
  
  function base64urlDecode(str: string): string {
    str = str.replace(/-/g, '+').replace(/_/g, '/');
    while (str.length % 4) {
      str += '=';
    }
    return atob(str);
  }
  
  function arrayBufferToBase64(buffer: ArrayBuffer): string {
    const bytes = new Uint8Array(buffer);
    let binary = '';
    for (let i = 0; i < bytes.byteLength; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
  }
  
  async function exportToPEM(key: CryptoKey, type: 'public' | 'private'): Promise<string> {
    const exported = await crypto.subtle.exportKey(
      type === 'public' ? 'spki' : 'pkcs8',
      key
    );
    const b64 = arrayBufferToBase64(exported);
    const pemType = type === 'public' ? 'PUBLIC KEY' : 'PRIVATE KEY';
    let pem = `-----BEGIN ${pemType}-----\n`;
    for (let i = 0; i < b64.length; i += 64) {
      pem += b64.substr(i, 64) + '\n';
    }
    pem += `-----END ${pemType}-----`;
    return pem;
  }
  
  async function generateKeyPair() {
    try {
      keyGenerationStatus = '⏳ Generating keys...';
      let keyPair: CryptoKeyPair;
      
      if (algorithm.startsWith('RS')) {
        const hashMap = {
          'RS256': 'SHA-256',
          'RS384': 'SHA-384',
          'RS512': 'SHA-512'
        };
        const modulusLengthMap = {
          'RS256': 2048,
          'RS384': 3072,
          'RS512': 4096
        };
        
        keyPair = await crypto.subtle.generateKey(
          {
            name: 'RSASSA-PKCS1-v1_5',
            modulusLength: modulusLengthMap[algorithm],
            publicExponent: new Uint8Array([1, 0, 1]),
            hash: hashMap[algorithm]
          },
          true,
          ['sign', 'verify']
        ) as CryptoKeyPair;
      } else if (algorithm.startsWith('ES')) {
        const curveMap = {
          'ES256': 'P-256',
          'ES384': 'P-384',
          'ES512': 'P-521'
        };
        
        keyPair = await crypto.subtle.generateKey(
          {
            name: 'ECDSA',
            namedCurve: curveMap[algorithm]
          },
          true,
          ['sign', 'verify']
        ) as CryptoKeyPair;
      } else if (algorithm.startsWith('PS')) {
        keyPair = await crypto.subtle.generateKey(
          {
            name: 'RSA-PSS',
            modulusLength: 2048,
            publicExponent: new Uint8Array([1, 0, 1]),
            hash: 'SHA-256'
          },
          true,
          ['sign', 'verify']
        ) as CryptoKeyPair;
      } else {
        throw new Error('Unsupported algorithm for key generation');
      }
      
      generatedKeyPair = keyPair;
      publicKey = await exportToPEM(keyPair.publicKey, 'public');
      privateKey = await exportToPEM(keyPair.privateKey, 'private');
      keyGenerationStatus = `✅ ${algorithm} keys generated successfully`;
    } catch (error) {
      keyGenerationStatus = '❌ ' + error.message;
    }
  }
  
  async function encodeToken() {
    try {
      const header = JSON.parse(headerInput);
      const payload = JSON.parse(payloadInput);
      
      header.alg = algorithm;
      headerInput = JSON.stringify(header, null, 2);
      
      const encodedHeader = base64urlEncode(JSON.stringify(header));
      const encodedPayload = base64urlEncode(JSON.stringify(payload));
      
      const dataToSign = `${encodedHeader}.${encodedPayload}`;
      const encoder = new TextEncoder();
      const messageData = encoder.encode(dataToSign);
      
      if (algorithm.startsWith('HS')) {
        const hashMap = {
          'HS256': 'SHA-256',
          'HS384': 'SHA-384',
          'HS512': 'SHA-512'
        };
        
        const keyData = encoder.encode(secretKey);
        
        const key = await crypto.subtle.importKey(
          'raw',
          keyData,
          { name: 'HMAC', hash: hashMap[algorithm] },
          false,
          ['sign']
        );
        
        const signature = await crypto.subtle.sign('HMAC', key, messageData);
        const signatureArray = new Uint8Array(signature);
        const signatureBase64 = base64urlEncode(
          String.fromCharCode(...signatureArray)
        );
        
        encodedToken = `${dataToSign}.${signatureBase64}`;
        verificationStatus = `✅ Token signed successfully with ${algorithm}`;
      } else if (algorithm.startsWith('RS') || algorithm.startsWith('ES') || algorithm.startsWith('PS')) {
        if (!generatedKeyPair) {
          throw new Error('Please generate keys first by clicking "Generate Keys" button');
        }
        
        const keyAlgorithm = generatedKeyPair.privateKey.algorithm as any;
        
        if (algorithm.startsWith('RS') && keyAlgorithm.name !== 'RSASSA-PKCS1-v1_5') {
          throw new Error(`Key mismatch: Generated ${keyAlgorithm.name} key, but selected ${algorithm}. Please regenerate keys.`);
        }
        if (algorithm.startsWith('ES') && keyAlgorithm.name !== 'ECDSA') {
          throw new Error(`Key mismatch: Generated ${keyAlgorithm.name} key, but selected ${algorithm}. Please regenerate keys.`);
        }
        if (algorithm.startsWith('PS') && keyAlgorithm.name !== 'RSA-PSS') {
          throw new Error(`Key mismatch: Generated ${keyAlgorithm.name} key, but selected ${algorithm}. Please regenerate keys.`);
        }
        
        let signature: ArrayBuffer;
        
        if (algorithm.startsWith('RS')) {
          const hashMap = {
            'RS256': 'SHA-256',
            'RS384': 'SHA-384',
            'RS512': 'SHA-512'
          };
          
          signature = await crypto.subtle.sign(
            {
              name: 'RSASSA-PKCS1-v1_5'
            },
            generatedKeyPair.privateKey,
            messageData
          );
        } else if (algorithm.startsWith('ES')) {
          const hashMap = {
            'ES256': 'SHA-256',
            'ES384': 'SHA-384',
            'ES512': 'SHA-512'
          };
          
          signature = await crypto.subtle.sign(
            {
              name: 'ECDSA',
              hash: hashMap[algorithm]
            },
            generatedKeyPair.privateKey,
            messageData
          );
        } else if (algorithm.startsWith('PS')) {
          signature = await crypto.subtle.sign(
            {
              name: 'RSA-PSS',
              saltLength: 32
            },
            generatedKeyPair.privateKey,
            messageData
          );
        }
        
        const signatureArray = new Uint8Array(signature);
        const signatureBase64 = base64urlEncode(
          String.fromCharCode(...signatureArray)
        );
        
        encodedToken = `${dataToSign}.${signatureBase64}`;
        verificationStatus = `✅ Token signed successfully with ${algorithm} (client-side WebCrypto)`;
      }
      
      decodeToken();
    } catch (error) {
      verificationStatus = '❌ ' + error.message;
    }
  }
  
  function decodeToken() {
    try {
      const parts = encodedToken.split('.');
      if (parts.length !== 3) {
        throw new Error('Invalid token format');
      }
      
      decodedHeader = JSON.stringify(
        JSON.parse(base64urlDecode(parts[0])), 
        null, 
        2
      );
      decodedPayload = JSON.stringify(
        JSON.parse(base64urlDecode(parts[1])), 
        null, 
        2
      );
      
      verificationStatus = '✅ Token decoded successfully';
    } catch (error) {
      verificationStatus = '❌ Invalid token format';
    }
  }
  
  function updateAlgorithm() {
    try {
      const header = JSON.parse(headerInput);
      header.alg = algorithm;
      headerInput = JSON.stringify(header, null, 2);
      
      if (!algorithm.startsWith('HS')) {
        generatedKeyPair = null;
        publicKey = '';
        privateKey = '';
        keyGenerationStatus = '';
      }
    } catch (e) {
      console.error('Invalid header JSON');
    }
  }
  
  $: if (algorithm) updateAlgorithm();
</script>

<div class="container mx-auto px-4 py-24">
  <h1 class="text-4xl font-bold mb-6 text-gradient">
    JWT Authentication Playground
  </h1>
  <p class="text-gray-400 mb-12 text-lg">
    Learn how JSON Web Tokens work by encoding, decoding, and understanding their structure
  </p>
  
  <div class="max-w-7xl mx-auto px-6">
  <div class="grid lg:grid-cols-2 gap-8 mb-12">
    <div class="card">
      <h3 class="text-2xl font-bold mb-4 text-white">🔧 Token Encoder</h3>
      
      <div class="mb-4">
        <label for="algorithm-select" class="block text-sm font-medium mb-2">Algorithm</label>
        <CustomSelect
          id="algorithm-select"
          bind:value={algorithm}
          options={[
            { value: 'HS256', label: 'HS256 (HMAC + SHA-256)', group: 'HMAC (Symmetric)' },
            { value: 'HS384', label: 'HS384 (HMAC + SHA-384)', group: 'HMAC (Symmetric)' },
            { value: 'HS512', label: 'HS512 (HMAC + SHA-512)', group: 'HMAC (Symmetric)' },
            { value: 'RS256', label: 'RS256 (RSA + SHA-256)', group: 'RSA (Asymmetric)' },
            { value: 'RS384', label: 'RS384 (RSA + SHA-384)', group: 'RSA (Asymmetric)' },
            { value: 'RS512', label: 'RS512 (RSA + SHA-512)', group: 'RSA (Asymmetric)' },
            { value: 'ES256', label: 'ES256 (ECDSA + P-256 + SHA-256)', group: 'ECDSA (Asymmetric)' },
            { value: 'ES384', label: 'ES384 (ECDSA + P-384 + SHA-384)', group: 'ECDSA (Asymmetric)' },
            { value: 'ES512', label: 'ES512 (ECDSA + P-521 + SHA-512)', group: 'ECDSA (Asymmetric)' },
            { value: 'PS256', label: 'PS256 (RSA-PSS + SHA-256)', group: 'RSA-PSS (Asymmetric)' }
          ]}
        />
      </div>
      
      <div class="mb-4">
        <label for="header-input" class="block text-sm font-medium mb-2">
          Header <span class="text-gray-400">(ALGORITHM & TOKEN TYPE)</span>
        </label>
        <textarea 
          id="header-input"
          bind:value={headerInput}
          class="w-full bg-gray-900 border border-white/20 rounded-lg px-4 py-2 font-mono text-sm h-24"
        ></textarea>
      </div>
      
      <div class="mb-4">
        <label for="payload-input" class="block text-sm font-medium mb-2">
          Payload <span class="text-gray-400">(DATA)</span>
        </label>
        <textarea 
          id="payload-input"
          bind:value={payloadInput}
          class="w-full bg-gray-900 border border-white/20 rounded-lg px-4 py-2 font-mono text-sm h-32"
        ></textarea>
      </div>
      
      <div class="mb-4">
        <label for="secret-input" class="block text-sm font-medium mb-2">
          {#if algorithm.startsWith('HS')}
            Secret Key <span class="text-gray-400">(HMAC SIGNATURE)</span>
          {:else}
            Cryptographic Keys <span class="text-gray-400">(WebCrypto)</span>
          {/if}
        </label>
        {#if algorithm.startsWith('HS')}
          <input 
            id="secret-input"
            bind:value={secretKey}
            type="password"
            class="w-full bg-gray-900 border border-white/20 rounded-xl px-4 py-3 font-mono text-sm"
          />
        {:else}
          <button on:click={generateKeyPair} class="btn-secondary w-full mb-3">
            🔑 Generate {algorithm} Key Pair
          </button>
          {#if keyGenerationStatus}
            <div class="mb-3 p-3 bg-gray-800 rounded-lg text-sm">
              {keyGenerationStatus}
            </div>
          {/if}
          {#if publicKey}
            <div class="mb-3">
              <div class="text-xs text-gray-400 mb-1">Public Key (PEM)</div>
              <textarea 
                readonly
                value={publicKey}
                class="w-full bg-gray-900 border border-white/20 rounded-lg px-3 py-2 font-mono text-xs h-32"
              ></textarea>
            </div>
          {/if}
          {#if privateKey}
            <div class="mb-3">
              <div class="text-xs text-gray-400 mb-1">Private Key (PEM)</div>
              <textarea 
                readonly
                value={privateKey}
                class="w-full bg-gray-900 border border-white/20 rounded-lg px-3 py-2 font-mono text-xs h-32"
              ></textarea>
            </div>
          {/if}
        {/if}
      </div>
      
      <button on:click={encodeToken} class="btn-primary w-full">
        🔐 Encode JWT Token
      </button>
      
      {#if verificationStatus}
        <div class="mt-4 p-3 bg-gray-800 rounded-lg text-sm">
          {verificationStatus}
        </div>
      {/if}
    </div>
    
    <div class="card">
      <h3 class="text-2xl font-bold mb-4 text-white">🔓 Encoded JWT Token</h3>
      
      <div class="mb-4">
        <label for="token-input" class="block text-sm font-medium mb-2">Paste JWT Token to Decode</label>
        <textarea 
          id="token-input"
          bind:value={encodedToken}
          on:input={decodeToken}
          placeholder="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
          class="w-full bg-gray-900 border border-gray-700 rounded-lg px-4 py-2 font-mono text-xs h-32 break-all"
        ></textarea>
      </div>
      
      {#if decodedHeader}
        <div class="mb-4">
          <div class="text-sm font-medium mb-2 text-white">Decoded Header</div>
          <pre class="bg-gray-900 border border-white/20 rounded-lg px-4 py-2 text-xs overflow-auto">{decodedHeader}</pre>
        </div>
      {/if}
      
      {#if decodedPayload}
        <div class="mb-4">
          <div class="text-sm font-medium mb-2 text-gray-300">Decoded Payload</div>
          <pre class="bg-gray-900 border border-white/20 rounded-lg px-4 py-2 text-xs overflow-auto">{decodedPayload}</pre>
        </div>
      {/if}
    </div>
  </div>
  
  <div class="card mb-8">
    <h3 class="text-3xl font-bold mb-6 text-white">🔐 All 10 Signing Algorithms</h3>
    
    <div class="mb-8">
      <h4 class="text-xl font-bold mb-4 text-white">HMAC Algorithms (Symmetric)</h4>
      <div class="grid md:grid-cols-3 gap-4">
        <div class="bg-white/5 border border-white/10 rounded-xl p-4">
          <h5 class="font-bold text-white mb-2">HS256</h5>
          <p class="text-sm text-gray-300">HMAC + SHA-256</p>
          <p class="text-xs text-gray-400 mt-2">256-bit hash</p>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-xl p-4">
          <h5 class="font-bold text-white mb-2">HS384</h5>
          <p class="text-sm text-gray-300">HMAC + SHA-384</p>
          <p class="text-xs text-gray-400 mt-2">384-bit hash</p>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-xl p-4">
          <h5 class="font-bold text-white mb-2">HS512</h5>
          <p class="text-sm text-gray-300">HMAC + SHA-512</p>
          <p class="text-xs text-gray-400 mt-2">512-bit hash (most secure)</p>
        </div>
      </div>
      <div class="mt-3 bg-white/5 border border-white/10 rounded-xl p-4">
        <p class="text-sm text-gray-300">
          <strong class="text-white">Symmetric:</strong> Same secret key for signing & verification • 
          <strong class="text-white">Speed:</strong> ⚡ Very fast • 
          <strong class="text-white">Use:</strong> Internal APIs, microservices
        </p>
      </div>
    </div>
    
    <div class="mb-8">
      <h4 class="text-xl font-bold mb-4 text-gray-200">RSA Algorithms (Asymmetric)</h4>
      <div class="grid md:grid-cols-3 gap-4">
        <div class="bg-white/5 border border-white/10 rounded-xl p-4">
          <h5 class="font-bold text-gray-200 mb-2">RS256</h5>
          <p class="text-sm text-gray-300">RSA + SHA-256</p>
          <p class="text-xs text-gray-400 mt-2">2048-bit key recommended</p>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-xl p-4">
          <h5 class="font-bold text-gray-200 mb-2">RS384</h5>
          <p class="text-sm text-gray-300">RSA + SHA-384</p>
          <p class="text-xs text-gray-400 mt-2">3072-bit key recommended</p>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-xl p-4">
          <h5 class="font-bold text-gray-200 mb-2">RS512</h5>
          <p class="text-sm text-gray-300">RSA + SHA-512</p>
          <p class="text-xs text-gray-400 mt-2">4096-bit key recommended</p>
        </div>
      </div>
      <div class="mt-3 bg-white/5 border border-white/10 rounded-xl p-4">
        <p class="text-sm text-gray-300">
          <strong class="text-gray-200">Asymmetric:</strong> Private key signs, public key verifies • 
          <strong class="text-gray-200">Speed:</strong> 🐢 Slower • 
          <strong class="text-gray-200">Use:</strong> OAuth, public APIs, third-party integrations
        </p>
      </div>
    </div>
    
    <div class="mb-8">
      <h4 class="text-xl font-bold mb-4 text-white">ECDSA Algorithms (Asymmetric)</h4>
      <div class="grid md:grid-cols-3 gap-4">
        <div class="bg-white/5 border border-white/10 rounded-xl p-4">
          <h5 class="font-bold text-white mb-2">ES256</h5>
          <p class="text-sm text-gray-300">ECDSA + P-256 + SHA-256</p>
          <p class="text-xs text-gray-400 mt-2">256-bit curve</p>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-xl p-4">
          <h5 class="font-bold text-white mb-2">ES384</h5>
          <p class="text-sm text-gray-300">ECDSA + P-384 + SHA-384</p>
          <p class="text-xs text-gray-400 mt-2">384-bit curve</p>
        </div>
        <div class="bg-white/5 border border-white/10 rounded-xl p-4">
          <h5 class="font-bold text-white mb-2">ES512</h5>
          <p class="text-sm text-gray-300">ECDSA + P-521 + SHA-512</p>
          <p class="text-xs text-gray-400 mt-2">521-bit curve</p>
        </div>
      </div>
      <div class="mt-3 bg-white/5 border border-white/10 rounded-xl p-4">
        <p class="text-sm text-gray-300">
          <strong class="text-white">Asymmetric:</strong> Elliptic curve cryptography • 
          <strong class="text-white">Speed:</strong> ⚡ Faster than RSA with same security • 
          <strong class="text-white">Use:</strong> Mobile apps, IoT, modern systems
        </p>
      </div>
    </div>
    
    <div class="mb-6">
      <h4 class="text-xl font-bold mb-4 text-gray-200">RSA-PSS Algorithm (Asymmetric)</h4>
      <div class="grid md:grid-cols-3 gap-4">
        <div class="bg-white/5 border border-white/10 rounded-xl p-4">
          <h5 class="font-bold text-gray-200 mb-2">PS256</h5>
          <p class="text-sm text-gray-300">RSA-PSS + SHA-256</p>
          <p class="text-xs text-gray-400 mt-2">Probabilistic signature scheme</p>
        </div>
      </div>
      <div class="mt-3 bg-white/5 border border-white/10 rounded-xl p-4">
        <p class="text-sm text-gray-300">
          <strong class="text-gray-200">Asymmetric:</strong> Enhanced RSA with randomized padding • 
          <strong class="text-gray-200">Speed:</strong> 🐢 Similar to RSA • 
          <strong class="text-gray-200">Use:</strong> High-security applications requiring provable security
        </p>
      </div>
    </div>
    
    <div class="bg-gray-800/50 border border-gray-700/50 rounded-2xl p-6">
      <h4 class="text-lg font-bold mb-3 text-white">🎯 Algorithm Selection Guide</h4>
      <div class="grid md:grid-cols-2 gap-4 text-sm text-gray-300">
        <div>
          <strong class="text-white">Choose HMAC (HS256/384/512) when:</strong>
          <ul class="mt-2 space-y-1 ml-4">
            <li>• Both parties can securely share a secret</li>
            <li>• Performance is critical (high-throughput)</li>
            <li>• Using within internal microservices</li>
            <li>• Simpler key management preferred</li>
          </ul>
        </div>
        <div>
          <strong class="text-gray-200">Choose RSA (RS256/384/512) when:</strong>
          <ul class="mt-2 space-y-1 ml-4">
            <li>• Distributing tokens to third parties</li>
            <li>• Multiple services verify tokens</li>
            <li>• Using with OAuth/OpenID Connect</li>
            <li>• Public key distribution needed</li>
          </ul>
        </div>
        <div>
          <strong class="text-white">Choose ECDSA (ES256/384/512) when:</strong>
          <ul class="mt-2 space-y-1 ml-4">
            <li>• Need smaller signatures than RSA</li>
            <li>• Working with mobile/IoT devices</li>
            <li>• Better performance required</li>
            <li>• Modern cryptography standards</li>
          </ul>
        </div>
        <div>
          <strong class="text-gray-200">Choose RSA-PSS (PS256) when:</strong>
          <ul class="mt-2 space-y-1 ml-4">
            <li>• Maximum security required</li>
            <li>• Provable security needed</li>
            <li>• Compliance requirements</li>
            <li>• Enhanced protection against attacks</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  
  <div class="card mb-8">
    <h3 class="text-3xl font-bold mb-6 text-white">📚 How JWT Works</h3>
    
    <div class="space-y-6">
      <div class="border-l-4 border-white/30 pl-6">
        <h4 class="text-xl font-bold mb-2 text-white">1. Header (Algorithm & Token Type)</h4>
        <p class="text-gray-400">
          The header contains metadata about the token, typically the algorithm used for signing (HS256, RS256) 
          and the token type (JWT). This is Base64URL encoded.
        </p>
        <code class="block mt-2 bg-gray-900 p-3 rounded text-sm text-white">
          {"{ \"alg\": \"HS256\", \"typ\": \"JWT\" }"}
        </code>
      </div>
      
      <div class="border-l-4 border-gray-500 pl-6">
        <h4 class="text-xl font-bold mb-2 text-gray-300">2. Payload (Claims/Data)</h4>
        <p class="text-gray-400">
          The payload contains the claims - statements about the user and additional data. 
          Standard claims include <code class="text-gray-300">sub</code> (subject), 
          <code class="text-gray-300">iat</code> (issued at), 
          <code class="text-gray-300">exp</code> (expiration time). This is also Base64URL encoded.
        </p>
        <code class="block mt-2 bg-gray-900 p-3 rounded text-sm text-gray-300">
          {"{ \"sub\": \"user123\", \"name\": \"John Doe\", \"iat\": 1516239022 }"}
        </code>
      </div>
      
      <div class="border-l-4 border-white/30 pl-6">
        <h4 class="text-xl font-bold mb-2 text-white">3. Signature (Verification)</h4>
        <p class="text-gray-400">
          The signature is created by encoding the header and payload, then signing them with a secret key 
          (HMAC) or private key (RSA). This ensures the token hasn't been tampered with.
        </p>
        <code class="block mt-2 bg-gray-900 p-3 rounded text-sm text-white">
          HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), secret)
        </code>
      </div>
      
      <div class="bg-white/5 border border-white/10 rounded-lg p-6">
        <h4 class="text-xl font-bold mb-3 text-white">🔒 Security Best Practices</h4>
        <ul class="space-y-2 text-gray-400">
          <li>✓ <strong>HS256:</strong> Symmetric - same key for signing and verification (simpler, faster)</li>
          <li>✓ <strong>RS256:</strong> Asymmetric - private key signs, public key verifies (more secure)</li>
          <li>✓ Always use HTTPS to transmit tokens</li>
          <li>✓ Set appropriate expiration times (exp claim)</li>
          <li>✓ Store tokens securely (httpOnly cookies or secure storage)</li>
          <li>✓ Never store sensitive data in the payload (it's just encoded, not encrypted)</li>
        </ul>
      </div>
      
      <div class="bg-white/5 border border-white/10 rounded-lg p-6">
        <h4 class="text-xl font-bold mb-3 text-gray-200">🔄 JWT Authentication Flow</h4>
        <div class="space-y-3 text-gray-400">
          <div class="flex items-start gap-3">
            <div class="bg-white/20 text-white rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-1">1</div>
            <p>User logs in with credentials → Server validates</p>
          </div>
          <div class="flex items-start gap-3">
            <div class="bg-white/20 text-white rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-1">2</div>
            <p>Server creates JWT with user info → Signs with secret key</p>
          </div>
          <div class="flex items-start gap-3">
            <div class="bg-white/20 text-white rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-1">3</div>
            <p>Server sends JWT to client → Client stores it</p>
          </div>
          <div class="flex items-start gap-3">
            <div class="bg-white/20 text-white rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-1">4</div>
            <p>Client sends JWT with each request → In Authorization header</p>
          </div>
          <div class="flex items-start gap-3">
            <div class="bg-white/20 text-white rounded-full w-6 h-6 flex items-center justify-center flex-shrink-0 mt-1">5</div>
            <p>Server verifies JWT signature → Grants/denies access</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</div>

<Footer />
