import streamlit as st
from langchain_helper import few_shots

st.title("AtliQ T Shirts: Database Q&A 👕")

question = st.text_input("Question : ")

if question:
    chain = few_shots()
    response = chain.run(question)

    st.header("Answer")
    st.write(response)

else :
    st.write("Enter valid  question")


    def main():
        st.title("Talk to Database : 👕")

    question = st.text_input("Enter your question:")
    if st.button("Ask"):
        if question:
            with st.spinner("Generating response..."):
                response = get_response(question)
            st.write("Response:", response)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()
