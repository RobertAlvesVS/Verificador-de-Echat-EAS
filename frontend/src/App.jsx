import React, { useState, useEffect } from "react";
import { io } from "socket.io-client";

const VerifySites = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Conectar ao servidor Socket.IO
    const socket = io("http://localhost:5000");

    // Ouvir o evento 'site_checked' do backend
    socket.on("site_checked", (data) => {
      setResults((prevResults) => [...prevResults, data]);
    });

    // Cleanup ao desmontar o componente
    return () => {
      socket.disconnect();
    };
  }, []);

  const startVerification = async () => {
    setLoading(true);
    setResults([]); // Limpa os resultados anteriores

    try {
      // Faz a chamada ao back-end para iniciar a verificação
      await fetch("http://localhost:5000/verify-site", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
    } catch (error) {
      console.error("Erro ao chamar o backend:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="text-center mt-5">
      <h1 className="text-3xl font-semibold mb-4">Verificar Sites</h1>
      <button
        onClick={startVerification}
        disabled={loading}
        className={`px-5 py-2 text-lg text-white rounded-lg ${
          loading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-blue-500 hover:bg-blue-700 cursor-pointer"
        }`}
      >
        {loading ? "Verificando..." : "Iniciar Verificação"}
      </button>

      <ul className="list-none p-0 mt-5">
        {results.map((result, index) => (
          <li
            key={index}
            className={`p-4 rounded-lg mb-2 ${
              result.element_present
                ? "bg-red-100 text-red-700 border-red-300"
                : "bg-green-100 text-green-700 border-green-300"
            } border`}
          >
            <a href={result.url} target="_blank" rel="noopener noreferrer">
              Me Click 👉{result.url}👈
            </a>
            :{" "}
            {result.element_present
              ? "Tema alguma conexão fora, favor verificar"
              : "Tudo certo por aqui"}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default VerifySites;
