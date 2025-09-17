"use client";

import { useState, useRef } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function Home() {
  const [messages, setMessages] = useState<{ sender: string; text: string }[]>([]);
  const [input, setInput] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleFileRemove = () => {
    setFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const handleFileUpload = async () => {
    if (!file) {
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      console.log(data);
      alert("File uploaded successfully!");
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
      alert("File upload failed.");
    }
  };

  const handleSend = async () => {
    if (input.trim()) {
      const userMessage = { sender: "user", text: input };
      setMessages((prevMessages) => [...prevMessages, userMessage]);
      setInput("");

      try {
        const response = await fetch("http://localhost:8000/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message: input }),
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        const botMessage = { sender: "bot", text: data.reply };
        setMessages((prevMessages) => [...prevMessages, botMessage]);
      } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
        const errorMessage = {
          sender: "bot",
          text: "Sorry, something went wrong.",
        };
        setMessages((prevMessages) => [...prevMessages, errorMessage]);
      }
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-b from-gray-900 to-black p-4">
      <Card className="w-full max-w-6xl border-0 bg-transparent">
        <CardHeader className="border-b border-gray-800/50">
          <CardTitle className="text-2xl font-bold text-white/90 mb-4">RAG Chatbot</CardTitle>
          <div className="flex items-center gap-3 pb-2">
            <div className="relative flex-1 max-w-xs">
              <input
                ref={fileInputRef}
                type="file"
                onChange={handleFileChange}
                className={`absolute inset-0 w-full h-full opacity-0 cursor-pointer ${!file ? 'z-10' : '-z-10'}`}
                accept=".pdf"
              />
              <Button
                variant="secondary"
                className="relative w-full bg-gray-800 hover:bg-gray-700 text-gray-200"
              >
                {file ? file.name : "Choose PDF File"}
              </Button>
            </div>
            {file && (
              <Button
                variant="ghost"
                size="icon"
                className="h-9 w-9 rounded-lg bg-red-500/10 text-red-400 hover:bg-gray-700 hover:text-red-300"
                onClick={handleFileRemove}
              >
                <span className="text-lg font-semibold">X</span>
              </Button>
            )}
            <Button
              onClick={handleFileUpload}
              disabled={!file}
              className="bg-blue-600 hover:bg-blue-500 text-white disabled:bg-gray-700"
            >
              Upload
            </Button>
          </div>
        </CardHeader>
        <CardContent className="p-6">
          <div className="space-y-4 h-[calc(70vh-80px)] overflow-y-auto pr-4 scrollbar-thin scrollbar-thumb-gray-700/50 scrollbar-track-transparent">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"
                  }`}
              >
                <div
                  className={`p-3 rounded-2xl max-w-[70%] shadow-lg ${message.sender === "user"
                    ? "bg-blue-600/90 text-white backdrop-blur-sm"
                    : "bg-gray-800/80 text-gray-200 backdrop-blur-sm"
                    }`}
                >
                  {message.text}
                </div>
              </div>
            ))}
          </div>
          <div className="flex gap-3 mt-4 bg-gray-800/50 p-4 rounded-xl backdrop-blur-sm">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === "Enter") {
                  handleSend();
                }
              }}
              placeholder="Type a message..."
              className="flex-grow bg-gray-800 border-gray-700 text-gray-200 placeholder:text-gray-400 focus:border-blue-500 h-12 text-lg"
            />
            <Button
              onClick={handleSend}
              className="bg-blue-600 hover:bg-blue-500 text-white px-8 rounded-lg h-12 text-lg font-medium"
            >
              Send
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
