import React, { useState } from 'react';
import axios from 'axios';

const Chatbot = () => {
  const [response, setResponse] = useState('');

  const handleChatRequest = async () => {
    try {
      const API_KEY = 'YOUR_API_KEY';
      const userPrompt = `
        User: How can you tell when to buy a stock? I'm new to investing.
        Assistant: Hello! I'd be happy to help you with your question. However, before we dive into specifics, I want to point out that it's important to consult with a financial advisor or professional before making any investment decisions. They can provide personalized advice based on your individual circumstances and risk tolerance.
        That being said, here are some general tips that may be helpful in determining when to buy a stock:
        Research the company: Before investing in a particular stock, research the company to understand its financials, business model, and growth prospects. Look for companies with strong fundamentals, such as a history of profitability, a competitive advantage, and a solid balance sheet.
        Evaluate market trends: Keep an eye on overall market trends and economic conditions. A strong economy with low inflation and stable interest rates can support stock prices. On the other hand, a recession or market downturn can lead to lower stock values.
        Consider valuation: Compare the stock's price to its earnings, revenue, and other fundamental metrics. Avoid overpaying for stocks by looking for value opportunities.
        Diversify your portfolio: Spread your investments across different asset classes, sectors, and geographic regions to minimize risk. This can help you ride out market volatility and capture growth opportunities in various areas.
        Have a long-term perspective: Investing in stocks should be a long-term game plan. Aim to hold onto your investments for at least five years or more, as this allows for the natural ebbs and flows of the market.
        Monitor news and events: Stay informed about news and events that may impact the stocks you own. Company announcements, industry developments, and macroeconomic factors can all influence stock performance.
        Be cautious of hype: Be wary of overhyped stocks or industries that promise unusually high returns. These situations can be risky and may not align with your investment goals.
        Consult multiple sources: Gather information from reliable sources, such as financial news outlets, research firms, and analyst reports. Avoid relying solely on one source or opinion.
        Be prepared to adapt: Your investment strategy may need to evolve over time based on changes in the market or your personal circumstances. Remain flexible and open to adjusting your approach as needed.
        Seek professional guidance: If you're new to investing or feel unsure about any aspect of the process, consider consulting a financial advisor or registered investment advisor. They can provide tailored advice and help you create a customized investment plan.
        Remember, there is no foolproof way to predict when to buy a specific stock. The best approach is to educate yourself on sound investing principles, remain patient, and be prepared to adapt to changing market conditions.
      `;

      const res = await axios.post('http://localhost:5000/chat-completion', { prompt: userPrompt }, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${API_KEY}`
        }
      });
      
      setResponse(res.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div>
      <button onClick={handleChatRequest}>Chat with Chatbot</button>
      <div>{response}</div>
    </div>
  );
};

export default Chatbot;
