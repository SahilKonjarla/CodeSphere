// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {

	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "CodeSphere" is now active!');

	// Hello World initial test 
	const disposable = vscode.commands.registerCommand('CodeSphere.helloWorld', () => {
		vscode.window.showInformationMessage('Hello World from CodeSphere!');
	});

	context.subscriptions.push(disposable);

	// Defining a chat handler
	const handler: vscode.ChatRequestHandler = async (
		request: vscode.ChatRequest,
		context: vscode.ChatContext,
		stream: vscode.ChatResponseStream,
		token: vscode.CancellationToken
	) => {
		return;
	};

	
}

// This method is called when your extension is deactivated
export function deactivate() {}
