/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/

import * as fs from 'fs';
import open from 'open';

const REQUEST1_URL = 'https://github.com/login/device/code';
const REQUEST2_URL = 'https://github.com/login/oauth/access_token';

// This is the VS Code OAuth app that the GitHub Authentication extension also uses
// This client ID is public and used for GitHub's OAuth device flow
const CLIENT_ID = '01ab8ac9400c4e429b23';

/**
 * Waits for a keypress from the user
 * Handles Ctrl+C gracefully to exit the process
 */
const keypress = async () => {
	if (process.stdin.isTTY) {
		process.stdin.setRawMode(true);
	}

	return new Promise<void>(resolve =>
		process.stdin.once('data', data => {
			const byteArray = [...data];
			if (byteArray.length > 0 && byteArray[0] === 3) {
				console.log('^C');
				process.exit(1);
			}
			if (process.stdin.isTTY) {
				process.stdin.setRawMode(false);
			}
			resolve();
		})
	);
};

/**
 * GitHub Copilot Token Setup Script
 * 
 * This script implements GitHub's OAuth 2.0 Device Authorization Grant flow
 * to obtain an access token for GitHub Copilot development and testing.
 * 
 * Flow:
 * 1. Request device code and user code from GitHub
 * 2. User authorizes the application via web browser
 * 3. Poll GitHub's token endpoint until authorization is complete
 * 4. Save the access token to .env file
 * 
 * Required Scopes:
 * - 'repo' - Needed for Copilot to access repository content and codesearch
 * 
 * Note: This token is for development/testing purposes. For production use,
 * consider using GitHub Apps or more specific scoped tokens.
 */
async function main(): Promise<void> {
	console.log('🚀 GitHub Copilot Token Setup');
	console.log('==============================');
	console.log('');
	console.log('This script will help you obtain a GitHub access token for Copilot development.');
	console.log('The token will be used for:');
	console.log('  • Accessing repository content');
	console.log('  • Code search functionality');
	console.log('  • Testing Copilot features');
	console.log('');

	// Step 1: Request device code from GitHub
	console.log('Step 1: Requesting device authorization...');
	const requestOptions: RequestInit = {
		method: 'POST',
		body: JSON.stringify({
			client_id: CLIENT_ID,
			// 'repo' scope is needed for Copilot to access private repos and enable codesearch
			scope: 'repo',
		}),
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
	};

	let request1Response;
	try {
		request1Response = await fetch(REQUEST1_URL, requestOptions);
		if (!request1Response.ok) {
			throw new Error(`HTTP ${request1Response.status}: ${request1Response.statusText}`);
		}
	} catch (error) {
		console.error('❌ Failed to request device code from GitHub');
		console.error('Check your internet connection and try again.');
		console.error('Error:', error);
		process.exit(1);
	}

	const response1 = (await request1Response.json()) as any;
	
	if (!response1.user_code || !response1.device_code) {
		console.error('❌ Invalid response from GitHub device authorization endpoint');
		console.error('Response:', response1);
		process.exit(1);
	}

	// Step 2: Display user code and instructions
	console.log('✅ Device authorization requested successfully');
	console.log('');
	console.log('📋 COPY THIS CODE: ' + response1.user_code);
	console.log('');
	console.log('Instructions:');
	console.log('1. Press any key to open GitHub in your browser');
	console.log('2. Paste the code above when prompted');
	console.log('3. Click "Continue" and then "Authorize" to approve access');
	console.log(`4. The token will be automatically retrieved within ${response1.interval} seconds after approval`);
	console.log('');
	console.log('⚠️  Note: The code expires in ' + Math.floor(response1.expires_in / 60) + ' minutes');
	console.log('');

	await keypress();

	// Step 3: Open GitHub authorization page
	console.log('🌐 Opening GitHub authorization page...');
	const timeout = new Promise((resolve) => setTimeout(resolve, 5000));
	try {
		await Promise.race([open(response1.verification_uri), timeout]);
		console.log(`📖 If the page didn't open automatically, please visit: ${response1.verification_uri}`);
	} catch (error) {
		console.log(`📖 Please manually navigate to: ${response1.verification_uri}`);
	}
	console.log('');

	// Step 4: Poll for access token
	console.log('⏳ Waiting for authorization...');
	let expiresIn = response1.expires_in;
	let accessToken: undefined | string;
	let attempts = 0;
	const maxAttempts = Math.floor(expiresIn / response1.interval);

	while (expiresIn > 0 && attempts < maxAttempts) {
		attempts++;
		const tokenRequestOptions: RequestInit = {
			method: 'POST',
			body: JSON.stringify({
				client_id: CLIENT_ID,
				device_code: response1.device_code,
				grant_type: 'urn:ietf:params:oauth:grant-type:device_code',
			}),
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
			},
		};

		try {
			const response2 = await fetch(REQUEST2_URL, tokenRequestOptions);
			const tokenResponse = (await response2.json()) as any;
			
			if (tokenResponse.access_token) {
				accessToken = tokenResponse.access_token;
				console.log('✅ Authorization successful!');
				break;
			} else if (tokenResponse.error === 'authorization_pending') {
				// Still waiting for user authorization
				process.stdout.write('⏳ ');
			} else if (tokenResponse.error === 'slow_down') {
				// GitHub is asking us to slow down our polling
				console.log('⏸️  Slowing down polling rate...');
				await new Promise(resolve => setTimeout(resolve, 1000));
			} else if (tokenResponse.error === 'expired_token') {
				console.log('❌ Device code has expired. Please run the script again.');
				process.exit(1);
			} else if (tokenResponse.error === 'access_denied') {
				console.log('❌ Authorization was denied. Please run the script again if you want to authorize.');
				process.exit(1);
			} else {
				console.log('⚠️  Unexpected response:', tokenResponse);
			}
		} catch (error) {
			console.error('❌ Error polling for token:', error);
		}

		expiresIn -= response1.interval;
		await new Promise(resolve => setTimeout(resolve, 1000 * response1.interval));
	}

	if (accessToken === undefined) {
		console.log('');
		console.log('❌ Timed out waiting for authorization');
		console.log('This can happen if:');
		console.log('  • You didn\'t complete the authorization in time');
		console.log('  • There was a network issue');
		console.log('  • The authorization was denied');
		console.log('');
		console.log('Please run the script again to try again.');
		process.exit(1);
	}

	// Step 5: Save token to .env file
	console.log('');
	console.log('💾 Saving token to .env file...');
	
	try {
		const raw = fs.existsSync('.env') ? fs.readFileSync('.env', 'utf8') : '';
		const result = raw.split('\n')
			.filter(line => !line.startsWith('GITHUB_OAUTH_TOKEN='))
			.concat([`GITHUB_OAUTH_TOKEN=${accessToken}`])
			.filter(line => line.trim() !== '') // Remove empty lines
			.join('\n');

		fs.writeFileSync('.env', result);
		console.log('✅ Token saved to .env file successfully');
		console.log('');
		console.log('🎉 Setup complete!');
		console.log('');
		console.log('Next steps:');
		console.log('  • You can now run tests and development commands');
		console.log('  • The token will be automatically used by the extension');
		console.log('  • To regenerate the token, run this script again');
		console.log('');
		console.log('📚 For more information about GitHub Copilot development:');
		console.log('  • See CONTRIBUTING.md for development guidelines');
		console.log('  • Visit https://docs.github.com/en/copilot for Copilot documentation');
		
		process.exit(0);
	} catch (error) {
		console.error('❌ Failed to save token to .env file');
		console.error('Error:', error);
		console.log('');
		console.log('You can manually add this line to your .env file:');
		console.log(`GITHUB_OAUTH_TOKEN=${accessToken}`);
		process.exit(1);
	}
}

// Only run if we're in a TTY environment (not in CI/automated systems)
if (!process.stdin.isTTY) {
	console.log('⚠️  Not running in a TTY environment, skipping token generation.');
	console.log('This script requires user interaction and cannot run in automated environments.');
	process.exit(0);
}

main().catch((error) => {
	console.error('❌ Unexpected error:', error);
	process.exit(1);
});
