
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, HttpUrl
import requests
from bs4 import BeautifulSoup
import spacy
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY not found in environment variables")

app = FastAPI()

nlp = spacy.load("en_core_web_sm")

class URLInput(BaseModel):
    url: HttpUrl

class ScrapingResult(BaseModel):
    industry: str | None
    company_size: str | None
    location: str | None


@app.post("/scrape", response_model=ScrapingResult)
async def scrape_homepage(url_input: URLInput, authorization: str = Header(...)):
    if authorization != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        response = requests.get(url_input.url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        text_content = soup.get_text().lower()

        industry = extract_industry(text_content)
        company_size = extract_company_size(text_content)
        location = extract_location(text_content)

        return ScrapingResult(industry=industry, company_size=company_size, location=location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the URL: {str(e)}")


import spacy

nlp = spacy.load("en_core_web_sm")

def extract_industry(text: str) -> str | None:
    doc = nlp(text)
    
    industry_keywords = {
        "Technology": ["technology", "software", "IT", "cloud", "artificial intelligence", "AI"],
        "Healthcare": ["health", "pharmaceutical", "medical", "healthcare", "biotech", "medicine"],
        "Finance": ["financial", "banking", "investment", "insurance", "fintech", "cryptocurrency"],
        "Education": ["education", "university", "college", "school", "learning", "training"],
        "Retail": ["retail", "shopping", "e-commerce", "store", "consumer goods", "fashion"],
        "Automotive": ["automotive", "car", "vehicle", "transportation", "motor", "automobile"],
    }

    for ent in doc.ents:
        if ent.label_ == "ORG":
            for industry, keywords in industry_keywords.items():
                if any(keyword.lower() in ent.text.lower() for keyword in keywords):
                    return industry

    for industry, keywords in industry_keywords.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):
            return industry

    return None




def extract_company_size(text: str) -> str | None:
    if "small company" in text or "startup" in text:
        return "Small"
    if "medium company" in text or "mid-size" in text:
        return "Medium"
    if "large company" in text or "enterprise" in text:
        return "Large"
    
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "ORG":
            if "small" in ent.text.lower():
                return "Small"
            elif "medium" in ent.text.lower():
                return "Medium"
            elif "large" in ent.text.lower():
                return "Large"
    return None


def extract_location(text: str) -> str | None:
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text
    return None



# from fastapi import FastAPI, HTTPException, Header
# from pydantic import BaseModel, HttpUrl
# import requests
# from bs4 import BeautifulSoup

# app = FastAPI()

# SECRET_KEY = "5e34696c683b438371cf6075fda45bda3313854582ab1b402344f0ddc16e13cc"

# class URLInput(BaseModel):
#     url: HttpUrl

# class ScrapingResult(BaseModel):
#     industry: str | None
#     company_size: str | None
#     location: str | None


# @app.post("/scrape", response_model=ScrapingResult)
# async def scrape_homepage(url_input: URLInput, authorization: str = Header(...)):
#     if authorization != SECRET_KEY:
#         raise HTTPException(status_code=401, detail="Unauthorized")

#     try:
#         response = requests.get(url_input.url, timeout=10)
#         response.raise_for_status()
#         soup = BeautifulSoup(response.text, "html.parser")

#         text_content = soup.get_text().lower()

#         industry = extract_industry(text_content)
#         company_size = extract_company_size(text_content)
#         location = extract_location(text_content)

#         return ScrapingResult(industry=industry, company_size=company_size, location=location)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing the URL: {str(e)}")


# def extract_industry(text: str) -> str | None:
#     if "technology" in text or "software" in text:
#         return "Technology"
#     if "health" in text or "pharmaceutical" in text:
#         return "Healthcare"
#     return None


# def extract_company_size(text: str) -> str | None:
#     if "small company" in text:
#         return "Small"
#     if "medium company" in text:
#         return "Medium"
#     if "large company" in text:
#         return "Large"
#     return None


# def extract_location(text: str) -> str | None:
#     for line in text.split("\n"):
#         if "location:" in line:
#             return line.split("location:")[1].strip()
#     return None
