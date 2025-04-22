import { useEffect, useRef, useState } from "react";
import { useChat } from "@ai-sdk/react";
import { v4 as uuidv4 } from "uuid";

export function Welcome() {
  const [chatId, setChatId] = useState<string>(uuidv4());
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const formRef = useRef<HTMLFormElement>(null);

  // Use the Vercel AI SDK for handling chat
  const { messages, input, handleInputChange, handleSubmit, status } = useChat({
    api: "http://localhost:8000/api/v1/chat",
    id: chatId.toString(),
    body: {
      chat_id: chatId,
    },
  });

  const isLoading = status === "submitted";

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const newChat = () => {
    setChatId(uuidv4());
    // Clear messages by forcing a re-mount of the component
    if (formRef.current) {
      formRef.current.reset();
    }
  };

  return (
    <main className="flex flex-col h-screen max-h-screen">
      {/* Header */}
      <header className="flex items-center justify-between px-4 py-3 border-b dark:border-gray-700">
        <h1 className="text-lg font-semibold text-gray-800 dark:text-white">
          AI Chat
        </h1>
        <button
          onClick={newChat}
          className="px-3 py-1 text-sm bg-blue-500 text-white rounded-md hover:bg-blue-600 transition"
        >
          New Chat
        </button>
      </header>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500 dark:text-gray-400">
            <div className="text-center max-w-md p-6 rounded-lg">
              <h2 className="text-2xl font-bold mb-4">Welcome to AI Chat</h2>
              <p className="mb-4">
                This is a simple chat application that uses AI to respond to
                your messages.
              </p>
              <p>Type a message below to get started.</p>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`rounded-lg px-4 py-2 max-w-[80%] ${
                  message.role === "user"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-200 dark:bg-gray-700 dark:text-white"
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Message Input */}
      <form
        ref={formRef}
        onSubmit={handleSubmit}
        className="border-t dark:border-gray-700 p-4"
      >
        <div className="flex items-center gap-2">
          <input
            className="flex-1 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-800 dark:border-gray-600 dark:text-white"
            value={input}
            onChange={handleInputChange}
            placeholder="Type a message..."
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? "..." : "Send"}
          </button>
        </div>
      </form>
    </main>
  );
}
