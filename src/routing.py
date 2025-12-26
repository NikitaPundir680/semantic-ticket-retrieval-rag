def routing_decision(query,df):
  results = semantic_search(query)
  categories = results["category"].tolist()
  unique_categories = set(categories)
  if len(unique_categories) == 1:
    decision = f"Route to {categories[0]} team"
    confidence = "High"
  else:
    decision = "Escalate to human (ambiguous issue)"
    confidence = "Low"
  return {
      "incoming_ticket": query,
      "similar_tickets": results[["message_text", "category", "similarity"]].to_dict(orient="records"),
      "final_decision": decision,
      "confidence": confidence
  }

output = routing_decision(
    "I cancelled my order but still no refund",
    df
)
output