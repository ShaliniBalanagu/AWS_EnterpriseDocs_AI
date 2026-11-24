from app.observability import trace
from typing import TypedDict,Any
from langgraph.graph import StateGraph,START,END
from app.aws import embed,answer
from app.vector import search
from app.config import settings
from guardrails import check_input,check_output

class State(TypedDict,total=False):
    question:str
    principal: Any
    passages:list
    answer:str
    sources:list
    status:str
    history:list

@trace("guard")
def guard(s):return {'question':check_input(s['question'])}

@trace("retrieve")
def retrieve(s):
    p=s['principal']
    # Include the most recent user question for short follow-ups such as 'summarize that'.
    prior_questions=[m['content'] for m in s.get('history',[]) if m['role']=='user']
    query=(prior_questions[-1]+'\nFollow-up: '+s['question']) if prior_questions else s['question']
    hits=search(p.tenant,embed(query),p.groups,p.subject)
    hits=[h for h in hits if h['score']>=settings().min_relevance]
    sources=[{'index':i+1,'document_id':h['metadata'].get('document_id',''),'title':h['metadata'].get('title',''), 'page':h['metadata'].get('page',1),'excerpt':h['metadata'].get('text','')[:320]} for i,h in enumerate(hits)]
    return {'passages':hits,'sources':sources}

