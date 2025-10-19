#!/usr/bin/env node

/**
 * Simple HTTP MCP Server for REST API Testing
 * Provides tools for making HTTP requests (GET, POST, PUT, DELETE)
 * For the Progressive Overload Log (P.O. Log) project
 */

const { McpServer } = require('mcp-framework');

const server = new McpServer({
  name: 'http-rest-api-server',
  version: '1.0.0'
});

// HTTP GET tool
server.addTool({
  name: 'http_get',
  description: 'Make HTTP GET requests to APIs',
  inputSchema: {
    type: 'object',
    properties: {
      url: {
        type: 'string',
        description: 'The URL to send the GET request to'
      },
      headers: {
        type: 'object',
        description: 'Optional headers to send with the request'
      }
    },
    required: ['url']
  }
}, async ({ url, headers = {} }) => {
  try {
    const fetch = await import('node-fetch').then(mod => mod.default);
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...headers
      }
    });
    
    const data = await response.text();
    return {
      status: response.status,
      statusText: response.statusText,
      headers: Object.fromEntries(response.headers),
      body: data
    };
  } catch (error) {
    return {
      error: error.message,
      status: 'ERROR'
    };
  }
});

// HTTP POST tool
server.addTool({
  name: 'http_post',
  description: 'Make HTTP POST requests to APIs',
  inputSchema: {
    type: 'object',
    properties: {
      url: {
        type: 'string',
        description: 'The URL to send the POST request to'
      },
      body: {
        type: 'object',
        description: 'The JSON body to send'
      },
      headers: {
        type: 'object',
        description: 'Optional headers to send with the request'
      }
    },
    required: ['url']
  }
}, async ({ url, body = {}, headers = {} }) => {
  try {
    const fetch = await import('node-fetch').then(mod => mod.default);
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...headers
      },
      body: JSON.stringify(body)
    });
    
    const data = await response.text();
    return {
      status: response.status,
      statusText: response.statusText,
      headers: Object.fromEntries(response.headers),
      body: data
    };
  } catch (error) {
    return {
      error: error.message,
      status: 'ERROR'
    };
  }
});

// HTTP PUT tool
server.addTool({
  name: 'http_put',
  description: 'Make HTTP PUT requests to APIs',
  inputSchema: {
    type: 'object',
    properties: {
      url: {
        type: 'string',
        description: 'The URL to send the PUT request to'
      },
      body: {
        type: 'object',
        description: 'The JSON body to send'
      },
      headers: {
        type: 'object',
        description: 'Optional headers to send with the request'
      }
    },
    required: ['url']
  }
}, async ({ url, body = {}, headers = {} }) => {
  try {
    const fetch = await import('node-fetch').then(mod => mod.default);
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...headers
      },
      body: JSON.stringify(body)
    });
    
    const data = await response.text();
    return {
      status: response.status,
      statusText: response.statusText,
      headers: Object.fromEntries(response.headers),
      body: data
    };
  } catch (error) {
    return {
      error: error.message,
      status: 'ERROR'
    };
  }
});

// HTTP DELETE tool
server.addTool({
  name: 'http_delete',
  description: 'Make HTTP DELETE requests to APIs',
  inputSchema: {
    type: 'object',
    properties: {
      url: {
        type: 'string',
        description: 'The URL to send the DELETE request to'
      },
      headers: {
        type: 'object',
        description: 'Optional headers to send with the request'
      }
    },
    required: ['url']
  }
}, async ({ url, headers = {} }) => {
  try {
    const fetch = await import('node-fetch').then(mod => mod.default);
    const response = await fetch(url, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...headers
      }
    });
    
    const data = await response.text();
    return {
      status: response.status,
      statusText: response.statusText,
      headers: Object.fromEntries(response.headers),
      body: data
    };
  } catch (error) {
    return {
      error: error.message,
      status: 'ERROR'
    };
  }
});

// Start the server
server.start().catch(console.error);