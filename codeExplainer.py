import streamlit as stream
import google.generativeai as gemini
import os
#function I
def configureKey(api_key):
	try:
		gemini.configure(api_key=api_key)
		return True
	except Exception as e:
		stream.error(f"Error configuring API: {e}")
		return False
#confirms whether the user enters an api key
#function II
def getExplanation(code, language):
	model=gemini.GenerativeModel("models/gemini-2.5-flash")
	prompt=f"""
	You are an expert programming instructor. Please explain the following {language} code snippet clearly and concisely. Structure your code exactly as follows:
	1. **Summary**: A 1-2 sentence high level overview of what the code does.
	2. **Key functions, variables, or components**: Briefly list the functions, variables and components used in the given code snippet.
	3. **Data flow**: A 1-2 line flowchart of how data flows(eg., input → processing → output).
	4. **Important logic concepts**: Briefly list the important programming concepts used(eg., loops, recursion, list comprehensions).
	5. **Block-by-block-breakdown**: Go through the program and explain what each significant block technically does in detail using bullet points, but avoid vague statements(eg., this handles logic).
	6. **Improvements & Sugggestions**: Briefly list at least 2 improvements(eg., Better readability or structure, Error handling, Performance optimization, Security or scalability improvements).
	Code Snippet:
	...
	{code}
	...
	"""
	try:
		with stream.spinner("Analyzing code..."):
			response=model.generate_content(prompt)
			return response.text
	except Exception as e:
			return f"Error generating explanation: {e}"
#output display
#page configuration
stream.set_page_config(
	page_title="Code Explainer with Gemini",
	page_icon="",
	layout="wide")
#function III
def main():
	with stream.sidebar:
		stream.header("Settings")
		default_key=os.getenv("GOOGLE_API_KEY", "")
		api_key=stream.text_input(
			"Enter the Google Gemini API Key",
			value=default_key,
			type="password",
			help="Get your key from https://aistudio.google.com/app/apikey")
		stream.markdown("...")
		stream.markdown(
			"Built with [Streamlit](https:#streamlit.io) and "
			"[Google Gemini](https:#deepmind.google/technologies/gemini/).")
	stream.title("AI Code Explainer")
	stream.markdown("Paste a snippet of code below to explain how it works line-by-line.")
	column1, column2=stream.columns([1, 1])
	with column1:
		stream.subheader("Input Code")
		language=stream.selectbox(
			"Select language (Optional helper)",
			["Python", "JavaScript", "Java", "C", "C++", "HTML/CSS", "SQL", "Other"])
		code_input=stream.text_area(
			"Paste your code here:",
			height=400,
			placeholder="def helloWorld():\n\tprint('Hello, Streamlit!')")
		analyze_button=stream.button("Explain Code", type="primary", use_container_width=True)
	with column2:
		stream.subheader("Explanation")
		if analyze_button:
			if not api_key:
				stream.warning("Please enter your Gemini API key in the sidebar to proceed.")
			elif not code_input:
				stream.warning("Please paste some code to analyze.")
			else:
				if configureKey(api_key):
					explanation=getExplanation(code_input, language)
					stream.markdown(explanation)
#main function
if __name__=="__main__":
	main()
#main function call
