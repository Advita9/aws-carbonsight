// import { useState } from "react";

// export default function App() {
//   const [input, setInput] = useState("");
//   const [response, setResponse] = useState("");
//   const [modelUsed, setModelUsed] = useState("");

//   const handleSend = async () => {
// 	  if (!input.trim()) return;

// 	  try {
// 	const res = await fetch("https://h3q23f94sb.execute-api.ap-southeast-2.amazonaws.com/ask", {
// 	  method: "POST",
// 	  headers: { "Content-Type": "application/json" },
// 	  body: JSON.stringify({ prompt: input }),
// 	});

// 	const rawText = await res.text();
// 	console.log("RAW TEXT:", rawText);

// 	let parsedBackend;
// 	try {
// 	  parsedBackend = JSON.parse(rawText);
// 	} catch (err) {
// 	  console.error("Could not parse backend JSON:", err);
// 	  setResponse("❌ Backend returned invalid JSON.");
// 	  return;
// 	}

// 	setResponse(parsedBackend.response);
// 	setModelUsed(parsedBackend.modelUsed);

// 	 }  catch (err) {
// 	    console.error("Frontend error:", err);
// 	    setResponse("⚠️ Error contacting backend.");
// 	  }

// 	};

//   return (
//     <div style={{ padding: "40px", color: "white" }}>
//       <h1>Carbonsight ♻️</h1>

//       <textarea
//         value={input}
//         onChange={(e) => setInput(e.target.value)}
//         placeholder="Type your question..."
//         style={{
//           width: "100%",
//           height: "150px",
//           background: "#222",
//           color: "white",
//           padding: "20px",
//           borderRadius: "12px",
//           fontSize: "18px",
//         }}
//       />

//       <button
//         onClick={handleSend}
//         style={{
//           marginTop: "20px",
//           padding: "12px 30px",
//           background: "#7CF68D",
//           borderRadius: "10px",
//           border: "none",
//           fontSize: "20px",
//           fontWeight: "bold",
//         }}
//       >
//         Send
//       </button>

//       <div style={{ marginTop: "40px" }}>
//         <h2>Model Response</h2>
//         <p>{response}</p>

//         <h3>Model Used:</h3>
//         <p>{modelUsed}</p>
//       </div>
//     </div>
//   );
// }


// import { useState } from "react";
// import ReactMarkdown from "react-markdown";

// export default function App() {
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState("");

//   const sendMessage = async () => {
//   if (!input.trim()) return;

//   const userMessage = { role: "user", text: input };
//   setMessages((m) => [...m, userMessage]);

//   try {
//     const res = await fetch(
//       "https://h3q23f94sb.execute-api.ap-southeast-2.amazonaws.com/ask",
//       {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ prompt: input }),
//       }
//     );

//     // STEP 1 — Read backend RAW TEXT
//     const rawText = await res.text();
//     console.log("RAW RESPONSE:", rawText);

//     let backend;

//     // STEP 2 — Parse raw JSON safely
//     try {
//       backend = JSON.parse(rawText);
//     } catch (err) {
//       console.error("❌ Could not parse raw backend JSON:", err);
//       setMessages((m) => [
//         ...m,
//         { role: "assistant", text: "⚠️ Backend returned invalid JSON." },
//       ]);
//       return;
//     }

//     // STEP 3 — Handle API Gateway case: body is a string containing JSON
//     let parsed = backend;
//     if (backend.body) {
//       try {
//         parsed = JSON.parse(backend.body);
//       } catch (err) {
//         console.error("❌ Could not parse backend.body JSON:", err);
//       }
//     }

//     // STEP 4 — Create assistant message
//     const botMessage = {
//       role: "assistant",
//       text: parsed.response || "⚠️ No response from backend",
//       model: parsed.modelUsed || "",
//     };

//     setMessages((m) => [...m, botMessage]);
//   } catch (err) {
//     console.error("Frontend error:", err);

//     setMessages((m) => [
//       ...m,
//       { role: "assistant", text: "⚠️ Error contacting backend." },
//     ]);
//   }

//   setInput("");
// };


//   return (
//     <div className="h-screen w-screen bg-[#0E0F10] text-white flex">

//       {/* LEFT SIDEBAR */}
//       <aside className="w-64 border-r border-white/10 p-4 hidden md:flex flex-col">
//         <h1 className="text-2xl font-semibold mb-6">Carbonsight ♻️</h1>

//         <h2 className="text-sm text-white/50 mb-2">Recent</h2>
//         <div className="space-y-2 flex-1 overflow-y-auto">
//           <p className="text-white/70">• Coming soon...</p>
//         </div>

//         <div className="mt-4 text-xs text-white/40">
//           Green AI for enterprises
//         </div>
//       </aside>

//       {/* MAIN CHAT PANEL */}
//       <main className="flex-1 flex flex-col h-screen">

//         {/* Chat messages */}
//         <div className="flex-1 overflow-y-auto p-8 space-y-6">

//           {messages.map((msg, idx) => (
//             <div key={idx} className="flex flex-col max-w-3xl">

//               <div
//                 className={`p-4 rounded-2xl text-sm leading-7 ${
//                   msg.role === "user"
//                     ? "self-end bg-blue-600/30"
//                     : "self-start bg-white/5"
//                 }`}
//               >
//                 {/* {msg.text} */}
//                 <ReactMarkdown
//                   components={{
//                     p: ({ children }) => (
//                       <p className="mb-3 leading-relaxed">{children}</p>
//                     ),
//                     h1: ({ children }) => (
//                       <h1 className="text-2xl font-bold mt-4 mb-2">{children}</h1>
//                     ),
//                     h2: ({ children }) => (
//                       <h2 className="text-xl font-semibold mt-4 mb-2">{children}</h2>
//                     ),
//                     h3: ({ children }) => (
//                       <h3 className="text-lg font-medium mt-3 mb-1">{children}</h3>
//                     ),
//                     ul: ({ children }) => (
//                       <ul className="list-disc ml-6 space-y-1">{children}</ul>
//                     ),
//                     li: ({ children }) => (
//                       <li className="">{children}</li>
//                     ),
//                   }}
//                 >
//                   {msg.text}
//                 </ReactMarkdown>


//               </div>

//               {msg.model && (
//                 <span className="text-xs text-white/40 mt-1">
//                   Model: {msg.model}
//                 </span>
//               )}
//             </div>
//           ))}

//         </div>

//         {/* INPUT BAR (Claude-style) */}
//         <div className="p-6 border-t border-white/10 bg-[#0F1012]">
//           <div className="max-w-3xl mx-auto flex items-center gap-3 bg-[#1A1C1E] p-4 rounded-xl">

//             <textarea
//               className="flex-1 bg-transparent outline-none resize-none text-sm"
//               placeholder="Ask Carbonsight anything..."
//               rows="1"
//               value={input}
//               onChange={(e) => setInput(e.target.value)}
//             />

//             <button
//               onClick={sendMessage}
//               className="px-4 py-2 bg-green-500 text-black font-semibold rounded-lg hover:bg-green-400"
//             >
//               Send
//             </button>

//           </div>
//         </div>

//       </main>
//     </div>
//   );
// }




  // const sendMessage = async () => {
  //   if (!input.trim()) return;

  //   const userMessage = { role: "user", text: input };
  //   setMessages((prev) => [...prev, userMessage]);

  //   try {
  //     const res = await fetch(
  //       "https://h3q23f94sb.execute-api.ap-southeast-2.amazonaws.com/ask",
  //       {
  //         method: "POST",
  //         headers: { "Content-Type": "application/json" },
  //         body: JSON.stringify({ prompt: input }),
  //       }
  //     );

  //     const raw = await res.text();
  //     let backend = JSON.parse(raw);
  //     let parsed = backend.body ? JSON.parse(backend.body) : backend;

  //     const assistantMessage = {
  //       role: "assistant",
  //       text: parsed.response,
  //       model: parsed.modelUsed,
  //       cached: parsed.cached || false,
  //       carbon: parsed.carbon
  //       ? {
  //           predicted_kwh: parsed.carbon.predicted_kwh,
  //           actual_kwh: parsed.carbon.actual_kwh,
  //           predicted_co2: parsed.carbon.predicted_co2,
  //           actual_co2: parsed.carbon.actual_co2
  //         }
  //       : null

  //     };

  //     setMessages((prev) => [...prev, assistantMessage]);

  //     setModelUsed(parsed.modelUsed);
  //     setCarbonData(parsed.carbon || null);

  //   } catch (err) {
  //     setMessages((prev) => [
  //       ...prev,
  //       { role: "assistant", text: " Error contacting backend." },
  //     ]);
  //   }

  //   setInput("");
  // };


    // 1️If optimize is ON → call backend /optimize
    // if (optimizePrompt) {
    //   try {
    //     const optRes = await fetch(
    //       "https://h3q23f94sb.execute-api.ap-southeast-2.amazonaws.com/optimize",
    //       {
    //         method: "POST",
    //         headers: { "Content-Type": "application/json" },
    //         body: JSON.stringify({ prompt: input }),
    //       }
    //     );

    //     const optRaw = await optRes.text();
    //     const optBackend = JSON.parse(optRaw);
    //     const optimized = optBackend.body ? JSON.parse(optBackend.body) : optBackend;

    //     finalPrompt = optimized.optimized;

    //     // insert system message showing optimized prompt
    //     setMessages(prev => [
    //       ...prev,
    //       { role: "system", text: `🔧 Optimized prompt → "${finalPrompt}"` }
    //     ]);

    //   } catch (err) {
    //     console.error("Optimization failed:", err);
    //   }
    // }

//     // 2️⃣ Add user message
//     const userMessage = { role: "user", text: finalPrompt };
//     setMessages(prev => [...prev, userMessage]);

//     // 3️⃣ Call ASK endpoint as usual
//     try {
//       const res = await fetch(
//         "https://h3q23f94sb.execute-api.ap-southeast-2.amazonaws.com/ask",
//         {
//           method: "POST",
//           headers: { "Content-Type": "application/json" },
//           body: JSON.stringify({ prompt: finalPrompt }),
//         }
//       );

//       const raw = await res.text();
//       let backend = JSON.parse(raw);
//       let parsed = backend.body ? JSON.parse(backend.body) : backend;

//       const assistantMessage = {
//         role: "assistant",
//         text: parsed.response,
//         model: parsed.modelUsed,
//         cached: parsed.cached || false,
//         carbon: parsed.carbon ? {
//           predicted_kwh: parsed.carbon.predicted_kwh,
//           actual_kwh: parsed.carbon.actual_kwh,
//           predicted_co2: parsed.carbon.predicted_co2,
//           actual_co2: parsed.carbon.actual_co2
//         } : null
//       };
//       // ✨ Insert optimized chip as a separate UI element
//       if (parsed.optimized) {
//         setMessages(prev => [
//           ...prev,
//           { 
//             role: "optimize-chip",
//             optimized: parsed.optimized,
//             savings_kwh: parsed.energy_savings_kwh,
//             savings_co2: parsed.co2_savings_kg
//           },
//           assistantMessage
//         ]);
//       } else {
//         setMessages(prev => [...prev, assistantMessage]);
//       }

//       setMessages(prev => [...prev, assistantMessage]);
//       setModelUsed(parsed.modelUsed);
//       setCarbonData(parsed.carbon || null);

//     } catch (err) {
//       console.error(err);
//       setMessages(prev => [
//         ...prev,
//         { role: "assistant", text: "⚠️ Error contacting backend." }
//       ]);
//     }

//     setInput("");
//   };


//   return (
//     <div className="h-screen w-screen bg-[#0E0F10] text-white flex flex-col">

//       {/* NAVBAR */}
//       <Navbar 
//         carbonData={carbonData} 
//         modelUsed={modelUsed} 
//         isCached={
//           [...messages].reverse().find(m => m.role === "assistant")?.cached || false
//         }
//  />

//       <div className="flex flex-1 overflow-hidden">

//         {/* SIDEBAR */}
//         <Sidebar history={messages} />

//         {/* MAIN CHAT PANEL */}
//         <main className="flex-1 flex flex-col h-full">

//           {/* Messages */}
//           <div className="flex-1 overflow-y-auto p-8 space-y-6">
//             {messages.map((msg, idx) => (
//               <div
//                 key={idx}
//                 className="relative group flex flex-col max-w-3xl"
//               >
//                 {/* MESSAGE BUBBLE */}
//                 <div
//                   className={`p-4 rounded-2xl text-sm leading-7 ${
//                     msg.role === "user"
//                       ? "self-end bg-blue-600/30"
//                       : "self-start bg-white/5"
//                   }`}
//                 >
//                   <div className="prose prose-invert max-w-none">
//                     <ReactMarkdown>{msg.text}</ReactMarkdown>
//                   </div>
//                 </div>

//                 {/* Cache Label */}
//                 {msg.cached && (
//                   <span className="text-xs text-green-400 font-semibold mt-1">
//                     ✓ Served from cache
//                   </span>
//                 )}

//                 {/* Model Label */}
//                 {msg.model && (
//                   <span className="text-xs text-white/40">
//                     Model: {msg.model}
//                   </span>
//                 )}

//                 {/* HOVER TOOLTIP (assistant messages only) */}
//                 {msg.role === "assistant" && (
//                   <div className="hidden group-hover:block absolute left-0 top-full z-50">
//                     <CarbonTooltip data={msg} />
//                   </div>
//                 )}

//               </div>
//             ))}

//           </div>



//           {/* INPUT */}
//           <div className="p-6 border-t border-white/10 bg-[#0F1012]">
//             <div className="max-w-3xl mx-auto flex items-center gap-3 bg-[#1A1C1E] p-4 rounded-xl">

//               <textarea
//                 className="flex-1 bg-transparent outline-none resize-none text-sm"
//                 placeholder={
//                   optimizePrompt
//                     ? "Eco-Optimized Mode ON — your prompt will be rewritten…"
//                     : "Ask Carbonsight anything..."
//                 }
//                 rows="1"
//                 value={input}
//                 onChange={(e) => setInput(e.target.value)}
//               />

//               {/* OPTIMIZE TOGGLE */}
//               <button
//                 onClick={() => setOptimizePrompt(!optimizePrompt)}
//                 className={`
//                   px-3 py-2 rounded-lg text-xs font-semibold transition
//                   ${optimizePrompt ? "bg-green-500 text-black" : "bg-white/10 text-white/50"}
//                 `}
//               >
//                 Optimize
//               </button>

//               {/* SEND BUTTON */}
//               <button
//                 onClick={sendMessage}
//                 className="px-4 py-2 bg-green-500 text-black font-semibold rounded-lg hover:bg-green-400"
//               >
//                 Send
//               </button>
//             </div>
//           </div>


//         </main>

//       </div>
//     </div>
//   );
// }


import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import CarbonTooltip from "./components/CarbonTooltip";

import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import { loadHistory, saveHistory } from "./utils/history";
import OptimizedChip from "./components/OptimizedChip";
import PromptSuggestor from "./components/PromptSuggestor";
import CarbonForecastPanel from "./components/CarbonForecastPanel";
import EcoPlanPanel from "./components/EcoPlanPanel";

export default function App() {
  const [messages, setMessages] = useState(loadHistory());
  const [input, setInput] = useState("");
  const [carbonData, setCarbonData] = useState(null);
  const [modelUsed, setModelUsed] = useState("");
  const [optimizePrompt, setOptimizePrompt] = useState(false);
  const [coachData, setCoachData] = useState(null);
  const [suggestMode, setSuggestMode] = useState(false);
  const [showForecast, setShowForecast] = useState(false);
  const [forecastData, setForecastData] = useState(null);
  const [ecoPlanMode, setEcoPlanMode] = useState(false);
  const [planData, setPlanData] = useState(null);
  const [isPlanning, setIsPlanning] = useState(false);
  const [planSteps, setPlanSteps] = useState([]);
  const [visibleSteps, setVisibleSteps] = useState([]);
  const [planLoading, setPlanLoading] = useState(false);





  // Save chat history automatically
  useEffect(() => {
    saveHistory(messages);
  }, [messages]);

  
  const sendMessage = async () => {
  if (!input.trim()) return;

  let workingPrompt = input;
  let plan = null;

  /* 0️⃣ Clear suggest mode if active */
  if (suggestMode) {
    setCoachData(null);
    setSuggestMode(false);
  }

    // let plan = null;

    // /* ======================================
    //       0️⃣ If Suggest Mode is ON
    //   ====================================== */
    // // Important: Suggestor DOES NOT send message to backend.
    // // It is a UI-only assist, so sendMessage should behave normally.
    // if (suggestMode) {
    //   // User is sending final edited prompt → clear coach
    //   setCoachData(null);
    //   setSuggestMode(false);
    // }

    // /* ======================================
    //       1️⃣ PLAN MODE — call /plan first
    //   ====================================== */
    // if (ecoPlanMode) {
    //   try {
    //     const res = await fetch(
    //       "https://h3q23f94sb.execute-api.ap-southeast-2.amazonaws.com/plan",
    //       {
    //         method: "POST",
    //         headers: { "Content-Type": "application/json" },
    //         body: JSON.stringify({ prompt: input })
    //       }
    //     );

    //     const planData = await res.json();
    //     plan = planData.plan || [];

    //     // Render plan block BEFORE user message
    //     setMessages(prev => [
    //       ...prev,
    //       { role: "plan", steps: plan }
    //     ]);
    //   } catch (err) {
    //     console.error("Plan generation failed:", err);
    //   }
    // }

    /* ======================================
          2️⃣ OPTIMIZE MODE — call /optimize
      ====================================== */
    if (optimizePrompt) {
      try {
        const optRes = await fetch(
          "https://h3q23f94sb.execute-api.ap-southeast-2.amazonaws.com/optimize",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt: input }),
          }
        );

        const parsedOpt = await optRes.json();
        workingPrompt = parsedOpt.optimized;

        // Show optimized chip BEFORE user message
        setMessages(prev => [
          ...prev,
          {
            role: "optimize-chip",
            optimized: parsedOpt.optimized,
            savings_kwh: parsedOpt.energy_savings_kwh,
            savings_co2: parsedOpt.co2_savings_kg,
          }
        ]);

      } catch (err) {
        console.error("Optimization failed:", err);
      }
    }


  /* 1️⃣ ECO PLAN MODE */
  if (ecoPlanMode) {
    try {
      setPlanLoading(true);
      setPlanSteps([]);
      setVisibleSteps([]);

      const res = await fetch(
        "https://h3q23f94sb.execute-api.ap-southeast-2.amazonaws.com/plan",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ prompt: workingPrompt })
        }
      );

      const data = await res.json();
      const steps = data.plan || [];

      setPlanSteps(steps);

      // ⏳ fake "thinking" delay
      setTimeout(() => {
        setPlanLoading(false);

        // 🎬 reveal steps one by one
        steps.forEach((step, index) => {
          setTimeout(() => {
            setVisibleSteps(prev => [...prev, step]);
          }, index * 700); // stagger animation
        });

      }, 1200);

    } catch (err) {
      console.error("Plan generation failed:", err);
      setPlanLoading(false);
    }
  }


    /* ======================================
          3️⃣ Add USER message
      ====================================== */
    setMessages(prev => [...prev, { role: "user", text: input }]);

    /* ======================================
          4️⃣ Call /ask with plan (optional)
      ====================================== */
    try {
      const res = await fetch(
        "https://h3q23f94sb.execute-api.ap-southeast-2.amazonaws.com/ask",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            prompt: workingPrompt,
            plan: ecoPlanMode ? plan : null   // only include plan when enabled
          }),
        }
      );

      const raw = await res.text();
      const backend = JSON.parse(raw);
      const parsed = backend.body ? JSON.parse(backend.body) : backend;

      const assistantMessage = {
        role: "assistant",
        text: parsed.response,
        model: parsed.modelUsed,
        cached: parsed.cached || false,
        carbon: parsed.carbon ? {
          predicted_kwh: parsed.carbon.predicted_kwh,
          actual_kwh: parsed.carbon.actual_kwh,
          predicted_co2: parsed.carbon.predicted_co2,
          actual_co2: parsed.carbon.actual_co2
        } : null
      };

      setMessages(prev => [...prev, assistantMessage]);

      setModelUsed(parsed.modelUsed);
      setCarbonData(parsed.carbon || null);

    } catch (err) {
      console.error(err);
      setMessages(prev => [
        ...prev,
        { role: "assistant", text: "⚠️ Error contacting backend." }
      ]);
    }

    setInput("");
  };


  const fetchForecast = async () => {
    try {
      const res = await fetch(
        "https://h3q23f94sb.execute-api.ap-southeast-2.amazonaws.com/forecast",
        { method: "GET" }
      );
      const data = await res.json();
      setForecastData(data);
    } catch (err) {
      console.error("Forecast fetch error:", err);
    }
  };


  return (
    <div className="h-screen w-screen bg-[#0E0F10] text-white flex flex-col">
      {/* NAVBAR */}
      <Navbar
        carbonData={carbonData}
        modelUsed={modelUsed}
        isCached={
          [...messages].reverse().find((m) => m.role === "assistant")?.cached ||
          false
        }
      />

      <div className="flex flex-1 overflow-hidden">
        {/* SIDEBAR */}
        <Sidebar history={messages} />

        {/* MAIN CHAT */}
        <main className="flex-1 flex flex-col h-full">
          <div className="flex-1 overflow-y-auto p-8 space-y-6">
            {messages.map((msg, idx) => {
              // 1️⃣ Special UI for optimize chip
              if (msg.role === "optimize-chip") {
                return (
                  <OptimizedChip 
                    key={idx}
                    optimized={msg.optimized}
                    savings_kwh={msg.savings_kwh}
                    savings_co2={msg.savings_co2}
                  />
                );
              }

              // 2️⃣ Normal messages
              return (
                <div key={idx} className="relative group flex flex-col max-w-3xl">
                  <div
                    className={`p-4 rounded-2xl text-sm leading-7 ${
                      msg.role === "user"
                        ? "self-end bg-blue-600/30"
                        : "self-start bg-white/5"
                    }`}
                  >
                    <div className="prose prose-invert max-w-none">
                      <ReactMarkdown>{msg.text}</ReactMarkdown>
                    </div>
                  </div>

                  {msg.cached && (
                    <span className="text-xs text-green-400 font-semibold mt-1">
                      ✓ Served from cache
                    </span>
                  )}

                  {msg.model && (
                    <span className="text-xs text-white/40">
                      Model: {msg.model}
                    </span>
                  )}

                  {msg.role === "assistant" && msg.carbon && (
                    <div className="hidden group-hover:block absolute left-0 top-full z-50">
                      <CarbonTooltip data={msg} />
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* INPUT PANEL */}
          <div className="p-6 border-t border-white/10 bg-[#0F1012]">
            <div className="max-w-3xl mx-auto flex items-center gap-3 bg-[#1A1C1E] p-4 rounded-xl">
              <textarea
                className="flex-1 bg-transparent outline-none resize-none text-sm"
                placeholder={
                  optimizePrompt
                    ? "R-EcoWrite — your prompt will be rewritten…"
                    : "Ask Carbonsight anything..."
                }
                rows="1"
                value={input}
                onChange={(e) => setInput(e.target.value)}
              />

              <button
                onClick={async () => {
                  if (suggestMode) {
                    // Turn off and clear suggestion
                    setCoachData(null);
                    setSuggestMode(false);
                    return;
                  }

                  // Turn ON: fetch suggestions
                  try {
                    const res = await fetch(
                      "https://h3q23f94sb.execute-api.ap-southeast-2.amazonaws.com/coach",
                      {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ prompt: input })
                      }
                    );

                    const data = await res.json();
                    setCoachData(data);
                    setSuggestMode(true);

                  } catch (err) {
                    console.error(err);
                  }
                }}
                className={`
                  px-3 py-2 rounded-lg text-xs font-semibold transition
                  ${suggestMode ? "bg-green-500 text-black" : "bg-white/10 text-white/60"}
                `}
              >
                Suggest
              </button>


              {/* OPTIMIZE TOGGLE */}
              <button
                onClick={() => setOptimizePrompt(!optimizePrompt)}
                className={`px-3 py-2 rounded-lg text-xs font-semibold transition ${
                  optimizePrompt
                    ? "bg-green-500 text-black"
                    : "bg-white/10 text-white/50"
                }`}
              >
                Optimize
              </button>

              <button
                onClick={() => setEcoPlanMode(!ecoPlanMode)}
                className={`px-3 py-2 rounded-lg text-xs font-semibold transition ${
                  ecoPlanMode ? "bg-purple-500 text-black" : "bg-white/10 text-white/60"
                }`}
              >
                Eco-Plan
              </button>


              {/* SEND */}
              <button
                onClick={sendMessage}
                className="px-4 py-2 bg-green-500 text-black font-semibold rounded-lg hover:bg-green-400"
              >
                Send
              </button>
            </div>
          </div>

          <PromptSuggestor
            coach={coachData}
            onClose={() => {
              setCoachData(null);
              setSuggestMode(false);
            }}
          />

        </main>

          {ecoPlanMode && (
  <EcoPlanPanel loading={planLoading} steps={visibleSteps} />
)}




      </div>

    </div>
  );
}
