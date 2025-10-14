import { Server } from "@modelcontextprotocol/sdk/server";

export default function({ sessionId, config }) {
  const server = new Server({
    name: "my-server",
    version: "1.0.0",
  });

  server.setRequestHandler("tools/list", async () => {
    return {
      tools: [
        {
          name: "add",
          description: "Add two numbers",
          inputSchema: {
            type: "object",
            properties: {
              a: { type: "number" },
              b: { type: "number" },
            },
            required: ["a", "b"],
          },
        },
      ],
    };
  });

  server.setRequestHandler("tools/call", async (request) => {
    const { name, arguments: args } = request.params;
    if (name === "add") {
      return {
        content: [
          {
            type: "text",
            text: String(args.a + args.b),
          },
        ],
      };
    }
    throw new Error(`Unknown tool: ${name}`);
  });

  return server;
};