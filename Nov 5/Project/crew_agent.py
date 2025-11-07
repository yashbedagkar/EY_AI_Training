import os
import re
import uuid
import json
import plotly.graph_objects as go
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAI
from tools.__web_search_tool import web_search_tool
from tools.__calculator_tool import calculator_tool
from chatbot import build_chatbot
from retriever import load_retriever
from langchain.memory import ConversationBufferMemory

# Prevent CrewAI from attempting OpenAI imports
os.environ["OPENAI_API_KEY"] = "DUMMY_KEY"

# -----------------------------
# ENVIRONMENT & SETUP
# -----------------------------
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Use Gemini for everything
gemini_llm = GoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

# Build RAG Chatbot & Retriever
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
rag_chatbot = build_chatbot(memory)
retriever = load_retriever(index_name="budget_faiss_index", k=6)


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def extract_number(text):
    """Extract first numeric value (int or float) from text."""
    if not text:
        return None
    match = re.search(r"\d+\.?\d*", str(text))
    return float(match.group()) if match else None


def check_rag_response_validity(response: str) -> bool:
    """Check if RAG response contains actual information or is a 'don't know' response."""
    # Common patterns indicating RAG doesn't have the answer
    no_info_patterns = [
        r"i don't know",
        r"don't have.*information",
        r"provided documents.*don't contain",
        r"cannot answer.*question",
        r"no information.*available",
        r"not mentioned.*documents",
        r"documents do not contain",
        r"unable to find.*information",
        r"not available in.*documents",
        r"can't find.*information",
        r"no data.*available",
        r"information.*not present"
    ]
    
    response_lower = response.lower().strip()
    
    # Check if response is too short (likely an error)
    if len(response_lower) < 20:
        return False
    
    # Check for specific "don't know" patterns
    for pattern in no_info_patterns:
        if re.search(pattern, response_lower):
            return False
    
    # If response contains substantial content and doesn't match negative patterns, it's valid
    return True


# -----------------------------
# SUMMARIZATION TOOL
# -----------------------------
def summarize_web_results(web_result: str, query: str) -> str:
    """Summarize web search results into a clear, concise answer."""
    summary_prompt = f"""
    Based on the following web search results, provide a clear and concise answer to the user's query.
    
    User Query: "{query}"
    
    Web Search Results:
    {web_result}
    
    Instructions:
    1. Extract key facts and figures
    2. Provide a well-structured, factual summary
    3. Keep the response concise but informative (max 200 words)
    4. If there are numerical data, present them clearly
    5. Use proper formatting for readability
    
    Provide only the summary, no preamble.
    """
    
    try:
        summary = gemini_llm.invoke(summary_prompt).strip()
        return summary
    except Exception as e:
        return f"Error summarizing results: {e}"


# -----------------------------
# TEXT TO VISUALIZATION INPUT CONVERTER
# -----------------------------
def convert_text_to_viz_input(text_data: str, query: str) -> dict:
    """Convert text data into structured input for visualization tool."""
    conversion_prompt = f"""
    You are a data extraction expert. Extract numerical data from the text and structure it for visualization.
    
    User Query: "{query}"
    
    Text Data:
    {text_data}
    
    Instructions:
    1. Identify all numerical values, categories, years, and metrics
    2. Structure the data as a JSON object
    3. Determine the best chart type (bar, line, pie, scatter, area, etc.)
    4. Format the response EXACTLY as shown below
    5. If the text says data is not available or cannot be visualized, return an empty data array
    
    Required JSON Format:
    {{
        "chart_type": "bar" or "line" or "pie" or "scatter" or "area",
        "title": "Appropriate chart title",
        "x_label": "X-axis label",
        "y_label": "Y-axis label",
        "data": [
            {{"label": "Category/Year 1", "value": 123.45}},
            {{"label": "Category/Year 2", "value": 234.56}}
        ]
    }}
    
    For multiple series/metrics, use this format:
    {{
        "chart_type": "line" or "bar",
        "title": "Chart title",
        "x_label": "X-axis label",
        "y_label": "Y-axis label",
        "series": [
            {{
                "name": "Series 1 name",
                "data": [{{"label": "Point 1", "value": 100}}, {{"label": "Point 2", "value": 120}}]
            }},
            {{
                "name": "Series 2 name",
                "data": [{{"label": "Point 1", "value": 90}}, {{"label": "Point 2", "value": 110}}]
            }}
        ]
    }}
    
    Return ONLY the JSON object, no explanations or markdown.
    """
    
    try:
        response = gemini_llm.invoke(conversion_prompt).strip()
        
        # Clean up response - remove markdown code blocks if present
        response = re.sub(r'^```json\s*', '', response)
        response = re.sub(r'^```\s*', '', response)
        response = re.sub(r'\s*```$', '', response)
        response = response.strip()
        
        # Parse JSON
        viz_input = json.loads(response)
        return viz_input
    except json.JSONDecodeError as e:
        print(f"⚠️ JSON parsing error: {e}")
        print(f"Raw response: {response}")
        return {
            "chart_type": "bar",
            "title": "Data Visualization",
            "x_label": "Category",
            "y_label": "Value",
            "data": []
        }
    except Exception as e:
        print(f"⚠️ Error converting to viz input: {e}")
        return {
            "chart_type": "bar",
            "title": "Data Visualization",
            "x_label": "Category",
            "y_label": "Value",
            "data": []
        }


# -----------------------------
# DYNAMIC VISUALIZATION TOOL
# -----------------------------
def visualization_tool(viz_input: dict) -> dict:
    """
    Generate dynamic visualizations based on structured input.
    Supports: bar, line, pie, scatter, area charts with single or multiple series.
    """
    
    try:
        # Check if data is empty
        if not viz_input.get("data") and not viz_input.get("series"):
            return {
                "success": False,
                "error": "No data available to visualize",
                "type": "error"
            }
        
        chart_type = viz_input.get("chart_type", "bar").lower()
        title = viz_input.get("title", "Data Visualization")
        x_label = viz_input.get("x_label", "Category")
        y_label = viz_input.get("y_label", "Value")
        
        fig = go.Figure()
        
        # Color palette
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
        # Check if it's multi-series data
        if "series" in viz_input:
            series_data = viz_input["series"]
            
            for idx, series in enumerate(series_data):
                series_name = series.get("name", f"Series {idx+1}")
                data_points = series.get("data", [])
                
                labels = [d.get("label", "") for d in data_points]
                values = [d.get("value", 0) for d in data_points]
                
                color = colors[idx % len(colors)]
                
                if chart_type == "line":
                    fig.add_trace(go.Scatter(
                        x=labels,
                        y=values,
                        mode='lines+markers',
                        name=series_name,
                        line=dict(color=color, width=3),
                        marker=dict(size=8)
                    ))
                elif chart_type == "bar":
                    fig.add_trace(go.Bar(
                        x=labels,
                        y=values,
                        name=series_name,
                        marker_color=color
                    ))
                elif chart_type == "area":
                    fig.add_trace(go.Scatter(
                        x=labels,
                        y=values,
                        mode='lines',
                        name=series_name,
                        fill='tozeroy',
                        line=dict(color=color, width=2)
                    ))
                elif chart_type == "scatter":
                    fig.add_trace(go.Scatter(
                        x=labels,
                        y=values,
                        mode='markers',
                        name=series_name,
                        marker=dict(size=12, color=color)
                    ))
        
        # Single series data
        else:
            data_points = viz_input.get("data", [])
            labels = [d.get("label", "") for d in data_points]
            values = [d.get("value", 0) for d in data_points]
            
            if chart_type == "pie":
                fig.add_trace(go.Pie(
                    labels=labels,
                    values=values,
                    marker=dict(colors=colors[:len(labels)]),
                    textinfo='label+percent',
                    textposition='auto'
                ))
            elif chart_type == "line":
                fig.add_trace(go.Scatter(
                    x=labels,
                    y=values,
                    mode='lines+markers',
                    line=dict(color=colors[0], width=3),
                    marker=dict(size=8, color=colors[0])
                ))
            elif chart_type == "bar":
                fig.add_trace(go.Bar(
                    x=labels,
                    y=values,
                    marker=dict(color=colors[:len(labels)])
                ))
            elif chart_type == "area":
                fig.add_trace(go.Scatter(
                    x=labels,
                    y=values,
                    mode='lines',
                    fill='tozeroy',
                    line=dict(color=colors[0], width=2)
                ))
            elif chart_type == "scatter":
                fig.add_trace(go.Scatter(
                    x=labels,
                    y=values,
                    mode='markers',
                    marker=dict(size=12, color=colors[:len(labels)])
                ))
            else:
                # Default to bar chart
                fig.add_trace(go.Bar(
                    x=labels,
                    y=values,
                    marker=dict(color=colors[:len(labels)])
                ))
        
        # Update layout
        layout_config = {
            'title': {
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#333333'}
            },
            'template': 'plotly_white',
            'showlegend': True,
            'hovermode': 'closest',
            'plot_bgcolor': 'rgba(240, 240, 240, 0.5)'
        }
        
        # Add axis labels for non-pie charts
        if chart_type != "pie":
            layout_config['xaxis'] = {
                'title': x_label,
                'showgrid': True,
                'gridcolor': 'rgba(200, 200, 200, 0.3)'
            }
            layout_config['yaxis'] = {
                'title': y_label,
                'showgrid': True,
                'gridcolor': 'rgba(200, 200, 200, 0.3)'
            }
        
        fig.update_layout(**layout_config)
        
        return {
            "success": True,
            "figure": fig,
            "key": f"viz_{uuid.uuid4().hex[:8]}",
            "type": "visualization"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Visualization error: {str(e)}",
            "type": "error"
        }


# -----------------------------
# MAIN ROUTING FUNCTION
# -----------------------------
def handle_user_query(query: str):
    """
    Enhanced intelligent routing with 5 decision paths:
    1. Calculator
    2. RAG only (no viz) - with fallback to web search
    3. Web search only (no viz)
    4. RAG + Visualization - with fallback to web search
    5. Web search + Visualization
    """
    
    routing_prompt = f"""
    Analyze the user's query and choose ONE of these 5 options:

    User Query: "{query}"

    Options:
    (1) CALCULATOR - Query requires arithmetic or percentage calculation
    (2) RAG_ONLY - Query is about India's Budget 2024-25/2025-26 and does NOT need visualization
    (3) WEB_ONLY - Query is NOT about budget documents, does NOT need visualization
    (4) RAG_VIZ - Query is about India's Budget 2024-25/2025-26 and NEEDS visualization (charts/graphs)
    (5) WEB_VIZ - Query is NOT about budget documents but NEEDS visualization (charts/graphs)

    Important Notes:
    - Budget-related topics include: fiscal deficit, budget allocations, schemes, taxes, customs duty, 
      tariffs, government spending, sectoral allocations, revenue, expenditure, budget estimates
    - Visualization keywords: chart, graph, plot, visualize, show trends, compare, display data, changes over time

    Respond with ONLY the number: 1, 2, 3, 4, or 5
    """
    
    try:
        decision = gemini_llm.invoke(routing_prompt).strip()
        # Extract first digit from response
        match = re.search(r'[1-5]', decision)
        if match:
            decision = match.group()
        else:
            decision = "2"  # Default to RAG_ONLY
    except Exception as e:
        print(f"⚠️ Routing error: {e}")
        decision = "2"
    
    print(f"\n🔹 Routing Decision: Path {decision}")
    
    # -----------------------------
    # PATH EXECUTION
    # -----------------------------
    try:
        # PATH 1: Calculator
        if decision == "1":
            print("  ↳ Using: Calculator Tool")
            result = calculator_tool(query)
            return {
                "type": "text",
                "content": f"🧮 **Calculator**\n\n{result}"
            }
        
        # PATH 2: RAG Only (No Visualization) - with fallback
        elif decision == "2":
            print("  ↳ Using: RAG Chatbot")
            rag_response = rag_chatbot.invoke({"question": query})
            
            # Check if RAG has valid information
            if check_rag_response_validity(rag_response):
                print("     ✓ RAG provided valid response")
                return {
                    "type": "text",
                    "content": f"🧠 **RAG Chatbot**\n\n{rag_response}"
                }
            else:
                print("     ⚠️ RAG doesn't have information, falling back to Web Search")
                web_result = web_search_tool(query)
                summary = summarize_web_results(web_result, query)
                return {
                    "type": "text",
                    "content": f"🌐 **Web Search** (RAG Fallback)\n\n{summary}"
                }
        
        # PATH 3: Web Search Only (No Visualization)
        elif decision == "3":
            print("  ↳ Using: Web Search → Summarization")
            web_result = web_search_tool(query)
            summary = summarize_web_results(web_result, query)
            return {
                "type": "text",
                "content": f"🌐 **Web Search**\n\n{summary}"
            }
        
        # PATH 4: RAG + Visualization - with fallback
        elif decision == "4":
            print("  ↳ Using: RAG → Text-to-Viz → Visualization")
            
            # Step 1: Get RAG response
            print("     • Step 1: Querying RAG chatbot...")
            rag_response = rag_chatbot.invoke({"question": query})
            
            # Check if RAG has valid information
            if not check_rag_response_validity(rag_response):
                print("     ⚠️ RAG doesn't have information, falling back to Web Search")
                print("  ↳ Switching to: Web Search → Summarization → Text-to-Viz → Visualization")
                
                # Fallback to web search path
                web_result = web_search_tool(query)
                summary = summarize_web_results(web_result, query)
                source_text = summary
                source_label = "🌐 **Web Search** (RAG Fallback)"
            else:
                print(f"     ✓ RAG response received")
                source_text = rag_response
                source_label = "🧠 **RAG Chatbot**"
            
            # Step 2: Convert to visualization input
            print("     • Step 2: Converting to visualization format...")
            viz_input = convert_text_to_viz_input(source_text, query)
            print(f"     ✓ Visualization input prepared")
            
            # Step 3: Create visualization
            print("     • Step 3: Generating visualization...")
            viz_result = visualization_tool(viz_input)
            
            if viz_result.get("success"):
                print("     ✓ Visualization created successfully!")
                
                return {
                    "type": "visualization",
                    "content": f"{source_label}\n\n📊 **Visualization Generated**\n\n{source_text}",
                    "figure": viz_result["figure"],
                    "key": viz_result["key"]
                }
            else:
                # If visualization fails, return text response
                return {
                    "type": "text",
                    "content": f"{source_label}\n\n{source_text}\n\n⚠️ Note: Visualization could not be generated - {viz_result.get('error', 'No data available')}"
                }
        
        # PATH 5: Web Search + Visualization
        elif decision == "5":
            print("  ↳ Using: Web Search → Summarization → Text-to-Viz → Visualization")
            
            # Step 1: Web search
            print("     • Step 1: Performing web search...")
            web_result = web_search_tool(query)
            print(f"     ✓ Web search completed")
            
            # Step 2: Summarize
            print("     • Step 2: Summarizing results...")
            summary = summarize_web_results(web_result, query)
            print(f"     ✓ Summary generated")
            
            # Step 3: Convert to visualization input
            print("     • Step 3: Converting to visualization format...")
            viz_input = convert_text_to_viz_input(summary, query)
            print(f"     ✓ Visualization input prepared")
            
            # Step 4: Create visualization
            print("     • Step 4: Generating visualization...")
            viz_result = visualization_tool(viz_input)
            
            if viz_result.get("success"):
                print("     ✓ Visualization created successfully!")
                
                return {
                    "type": "visualization",
                    "content": f"🌐 **Web Search**\n\n📊 **Visualization Generated**\n\n{summary}",
                    "figure": viz_result["figure"],
                    "key": viz_result["key"]
                }
            else:
                # If visualization fails, return text response
                return {
                    "type": "text",
                    "content": f"🌐 **Web Search**\n\n{summary}\n\n⚠️ Note: Visualization could not be generated - {viz_result.get('error', 'No data available')}"
                }
        
        else:
            return {
                "type": "text",
                "content": "❓ Sorry, I couldn't determine the appropriate tool for your query."
            }
    
    except Exception as e:
        return {
            "type": "text",
            "content": f"⚠️ Error during processing: {str(e)}"
        }


# -----------------------------
# INTERACTIVE CONSOLE LOOP
# -----------------------------
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🤖 India's Budget Agent - Enhanced with Dynamic Visualization")
    print("="*70)
    print("\n📊 Features:")
    print("  • RAG Chatbot for Budget 2024-25 & 2025-26")
    print("  • Web Search with Summarization")
    print("  • Advanced Calculator")
    print("  • Dynamic Visualization (Bar, Line, Pie, Scatter, Area charts)")
    print("  • Smart Fallback: RAG → Web Search if no info found")
    print("\n💡 Try queries like:")
    print("  - 'What is the fiscal deficit for 2025-26?'")
    print("  - 'Compare defense spending across years with a chart'")
    print("  - 'Calculate 15% of 50000'")
    print("  - 'Show me India's GDP growth trends'")
    print("\n" + "="*70 + "\n")
    
    while True:
        user_q = input("🧑 You: ")
        if user_q.lower().strip() in ["exit", "quit", "bye", "q"]:
            print("\n👋 Thank you for using India's Budget Agent. Goodbye!\n")
            break
        
        if not user_q.strip():
            continue
        
        result = handle_user_query(user_q)
        
        print("\n" + "-"*70)
        
        if result["type"] == "visualization":
            print(f"🤖 Agent:\n\n{result['content']}")
            print(f"\n🖼️ Chart Key: {result['key']}")
            print("\n📊 Displaying visualization...\n")
            result["figure"].show()
        else:
            print(f"🤖 Agent:\n\n{result['content']}")
        
        print("-"*70 + "\n")