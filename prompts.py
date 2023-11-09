from langchain.prompts import PromptTemplate

map_prompt = """The following is a document

{docs}

---

Imagine you are working on a mind map. 
Based on this list of docs, please create an insightful summary that will have some general ideas, but also specifics about the text.

You can use bullet points that will convey the general idea 

---
Helpful Summary:"""


reduce_prompt = """"You are an expert summarizer. Based on the following documetns you will create a summary. \n\n{docs}\n\nInsightful summary:"""


mindmap_prompt = """Imagine you are a professional mind map generator. You take a summary of a text and turn it into a mind map.
Here are some examples of Mermaid.js syntax.
---
Example 1:

mindmap
  root((mindmap))
    Origins
      Long history
      ::icon(fa fa-book)
      Popularisation
        British popular psychology author Tony Buzan
    Research
      On effectiveness<br/>and features
      On Automatic creation
        Uses
            Creative techniques
            Strategic planning
            Argument mapping
    Tools
      Pen and paper
      Mermaid
---
Example 2:

mindmap
    id1["`**Root** with
a second line
Unicode works too: 🤓`"]
      id2["`The dog in **the** hog... a *very long text* that wraps to a new line`"]
      id3[Regular labels still works]
---

Text summary:
{summary}

---

Based on the syntax examples and the text summary, create a mindmap about the text from the summary using the Mermaid.js syntax.

Helpful mindmap:
"""


map_template = PromptTemplate.from_template(map_prompt)
reduce_template = PromptTemplate.from_template(reduce_prompt)
mindmap_template = PromptTemplate.from_template(mindmap_prompt)
