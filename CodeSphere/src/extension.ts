// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import {v4 as uuidv4} from 'uuid';
import { error } from 'console';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
	// This line of code will only be executed once when your extension is activated
	console.log('Welcome to CodeSphere!');

	// Hello World initial test 
	const disposable = vscode.commands.registerCommand('CodeSphere.helloWorld', () => {
		vscode.window.showInformationMessage('Hello World from CodeSphere!');
	});

	context.subscriptions.push(disposable);

	// ##################################################################################
	// ##################################################################################
	// Chat Creation section

	// Define a key for storing the UUID in the workspace state
	const uuidKey = "codesphereUUID";

	// Get or create a new uuid from workspace state
	let userUUID = context.workspaceState.get<string>(uuidKey);
	if (!userUUID) {
		userUUID = uuidv4();
		context.workspaceState.update(uuidKey, userUUID);
		console.log(`Generated new UUID: ${userUUID}`);
	} else {
		console.log(`Retrieved existing UUID ${userUUID}`);
	}
	// Define a chat handler
	const handler: vscode.ChatRequestHandler = async (
		request: vscode.ChatRequest,
		context: vscode.ChatContext,
		stream: vscode.ChatResponseStream,
		token: vscode.CancellationToken
	) => {
		// Make the backend call to retrieve the response from the agents
		async function backendCall(userUUID: string, message: string): Promise<any> {
			try {
				const res = await fetch('http://localhost:8000/api/v1/orchestrator', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({
						"message": message,
						"user_id": userUUID,
						"additional_params": {}
					})
				});

				if (!res.ok) {
					throw new Error(`Server responded with ${res.status}: ${res.statusText}`);
				}

				const data = await res.json();
				return data;
			} catch (err) {
				console.error("API call failed", err);
				throw new Error(`Failed to communicate with the backend. Please try again`);
			}
		}

		// Await for the response from the backend
		const response = await backendCall(userUUID, request.prompt);

		// Parse the response and stream it to the chat
		const responseData = response[0];
		const errors = responseData.errors;
		const suggestions = responseData.suggestions;
		const explanation = responseData.explanation;

		// Stream the response to the chat
		if (errors.length > 0) {
			stream.markdown(errors.join('\n'));
		}

		if (suggestions.length > 0) {
			stream.markdown(suggestions.join('\n'));
		}

		// Stream explanation if they exist
		if (explanation.length > 0) {
			stream.markdown(explanation.join('\n'));
		}

		// Exit function
		return;
	};

	// Create the participant
	const assitant = vscode.chat.createChatParticipant('CodeSphere.code-assistant', handler);
}

// This method is called when your extension is deactivated
export function deactivate() {
	console.log("Goodbye! Thank you for using CodeSphere");
}
