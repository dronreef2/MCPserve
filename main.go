package main

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"os"

	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
)

func fetchTool(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	url, ok := request.Params.Arguments["url"].(string)
	if !ok {
		return nil, fmt.Errorf("url parameter is required")
	}

	jinaKey := os.Getenv("JINA_API_KEY")
	if jinaKey == "" {
		return mcp.NewToolResultError("JINA_API_KEY not set"), nil
	}

	req, err := http.NewRequestWithContext(ctx, "GET", "https://r.jina.ai/"+url, nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Authorization", "Bearer "+jinaKey)

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Error fetching %s: %v", url, err)), nil
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return mcp.NewToolResultError(fmt.Sprintf("Error fetching %s: %d", url, resp.StatusCode)), nil
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	return mcp.NewToolResultText(string(body)), nil
}

func searchTool(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	query, ok := request.Params.Arguments["query"].(string)
	if !ok {
		return nil, fmt.Errorf("query parameter is required")
	}

	jinaKey := os.Getenv("JINA_API_KEY")
	if jinaKey == "" {
		return mcp.NewToolResultError("JINA_API_KEY not set"), nil
	}

	req, err := http.NewRequestWithContext(ctx, "GET", "https://s.jina.ai/"+query, nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Authorization", "Bearer "+jinaKey)

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return mcp.NewToolResultError(fmt.Sprintf("Error searching %s: %v", query, err)), nil
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return mcp.NewToolResultError(fmt.Sprintf("Error searching %s: %d", query, resp.StatusCode)), nil
	}

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	return mcp.NewToolResultText(string(body)), nil
}

func translateTool(ctx context.Context, request mcp.CallToolRequest) (*mcp.CallToolResult, error) {
	text, ok := request.Params.Arguments["text"].(string)
	if !ok {
		return nil, fmt.Errorf("text parameter is required")
	}

	fromLang := "zh"
	toLang := "en"
	if fl, ok := request.Params.Arguments["from_lang"].(string); ok {
		fromLang = fl
	}
	if tl, ok := request.Params.Arguments["to_lang"].(string); ok {
		toLang = tl
	}

	// Simple translation placeholder - in real implementation, integrate with Gemini or DeepL
	result := fmt.Sprintf("[Translated from %s to %s]: %s", fromLang, toLang, text)
	return mcp.NewToolResultText(result), nil
}

func main() {
	srv := server.NewMCPServer(
		"ai-tools",
		"1.0.0",
	)

	srv.AddTool(mcp.NewTool("fetch",
		mcp.WithDescription("Fetch the content of a web page using Jina AI"),
		mcp.WithString("url", mcp.Required(), mcp.Description("The URL to fetch")),
	), fetchTool)

	srv.AddTool(mcp.NewTool("search",
		mcp.WithDescription("Search the web using Jina AI"),
		mcp.WithString("query", mcp.Required(), mcp.Description("The search query")),
	), searchTool)

	srv.AddTool(mcp.NewTool("translate",
		mcp.WithDescription("Translate text between languages"),
		mcp.WithString("text", mcp.Required(), mcp.Description("The text to translate")),
		mcp.WithString("from_lang", mcp.Description("Source language (default: zh)")),
		mcp.WithString("to_lang", mcp.Description("Target language (default: en)")),
	), translateTool)

	if err := server.ServeStdio(srv); err != nil {
		fmt.Fprintf(os.Stderr, "Server error: %v\n", err)
		os.Exit(1)
	}
}