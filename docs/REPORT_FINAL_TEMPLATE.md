# \# Hiver SDE Intern Take-Home

# 

# \## 1. Objective

# 

# The goal was to build a support copilot for AppleSupport that takes an incoming customer message and performs four tasks: classify the support intent, retrieve a similar resolved historical case, draft a conservative response grounded in that evidence, and decide whether the interaction can be auto-handled or should be escalated.

# 

# The design separates intent from escalation because the type of problem and the risk of handling it automatically are different decisions.

# 

# \## 2. Data

# 

# The Kaggle Customer Support on Twitter dataset was used. Customer/support pairs were reconstructed using tweet-response IDs.

# 

# AppleSupport was selected because it provided a large number of usable customer/support pairs and broad coverage of support issues. The resulting AppleSupport dataset contained 106,623 usable paired conversations.

# 

# A chronological 80/20 split was used:

# \- Training: 85,298 conversations

# \- Test: 21,325 conversations

# 

# The chronological split prevents future conversations from leaking into training when evaluating earlier/later support behavior.

# 

# A deterministic 200-example golden evaluation set was created from the held-out data and reviewed for evaluation labels. A separate 50-example qualitative review set was also used to assess retrieved evidence and drafted replies.

# 

# \## 3. Taxonomy

# 

# Eight intents were used:

# 

# 1\. `software\_update` — update, installation, restoration, or OS-update problems.

# 2\. `device\_performance` — crashes, freezing, instability, overheating, restarting, or general device problems.

# 3\. `app\_or\_feature\_issue` — malfunctioning Apple apps, features, or functionality.

# 4\. `connectivity` — Wi-Fi, Bluetooth, cellular, calls, or other connection problems.

# 5\. `account\_security` — account access, authentication, suspicious messages, phishing, or security issues.

# 6\. `purchase\_repair\_support` — purchases, repairs, replacements, trade-ins, damaged hardware, or service.

# 7\. `information\_request` — informational, compatibility, feature, or how-to questions.

# 8\. `unclear` — insufficient information to confidently determine an intent.

# 

# Escalation is modeled separately because intent and risk are not the same decision. Cases involving security, financial concerns, physical damage, repairs/replacements, possible data loss, severe instability, or insufficient information are treated more cautiously.

# 

# \## 4. Evaluation design

# 

# The classifier was trained using weak supervision and evaluated on a fixed 200-example golden set.

# 

# The baseline combines word and character TF-IDF features with balanced Logistic Regression. This was intentionally chosen as a simple, interpretable baseline that can be trained quickly and reproduced locally.

# 

# For response generation, the system retrieves a similar historical training example and uses its historical support answer as evidence for a conservative draft response.

# 

# The escalation layer uses explicit risk-oriented rules rather than treating escalation as another intent.

# 

# An additional LLM-as-judge harness evaluates generated replies on:

# \- helpfulness (1–5)

# \- correctness (1–5)

# \- clarity (1–5)

# \- evidence support (0/1)

# 

# The LLM judge was executed using Gemini through its OpenAI-compatible API interface.

# 

# \## 5. Results

# 

# | Metric | Result |

# |---|---:|

# | Golden examples | 200 |

# | Intent accuracy | 54.0% |

# | Escalation precision | 61.0% |

# | Escalation recall | 85.9% |

# | Escalation F1 | 71.3% |

# | Average retrieval similarity | 0.344 |

# | Average reply characters | 262.7 |

# | LLM-judged examples | 200 |

# | Human/LLM Cohen's kappa | 0.00 |

# 

# \### Intent classification

# 

# The classifier achieved 54.0% overall accuracy, with a macro F1 of 0.56 and weighted F1 of 0.54.

# 

# The strongest classes were:

# \- Connectivity: F1 0.75

# \- Account security: F1 0.71

# \- Software update: F1 0.61

# \- Device performance: F1 0.59

# 

# The weaker classes included:

# \- Purchase/repair support: F1 0.44

# \- Unclear: F1 0.44

# \- Information request: F1 0.45

# \- App/feature issue: F1 0.53

# 

# The escalation layer achieved 85.9% recall and 71.3% F1. The relatively high recall is desirable for a support copilot because missing a genuinely risky case can be more costly than escalating a routine case unnecessarily.

# 

# \### LLM evaluation and agreement

# 

# The LLM judge successfully evaluated all 200 golden replies.

# 

# Human/LLM evidence-support agreement was calculated on the overlapping labeled subset. Only 3 examples had valid labels from both judges, producing Cohen's kappa of 0.00. This sample is too small to support a reliable estimate of human/LLM agreement, so the result should be treated as an evaluation limitation rather than evidence that the judge is inherently unreliable.

# 

# \## 6. Failure analysis

# 

# \### A. Ambiguous short messages

# 

# Messages containing only a device/software version, a short complaint, or very little context are difficult to classify safely. These cases frequently fall into the `unclear` category or are absorbed into broad categories.

# 

# \### B. Multiple simultaneous symptoms

# 

# Customers can mention an update, battery issue, Wi-Fi problem, and app crash in the same message. A single-label taxonomy forces the system to choose one primary intent, which can lose important secondary context.

# 

# \### C. Retrieval mismatch

# 

# TF-IDF retrieval is based primarily on lexical similarity. This means a message can retrieve a historically similar example because it shares words with the query while actually describing a different underlying problem.

# 

# This is particularly important for support messages where the same terms can occur across unrelated issues.

# 

# \### D. Weak supervision

# 

# The training labels are generated using heuristic weak supervision rather than a large independently hand-labeled training set. This makes the baseline fast and reproducible but limits classification quality.

# 

# The results show this clearly: `software\_update` has high recall (0.92) but lower precision (0.46), while `unclear` has high recall (0.77) but low precision (0.31). This indicates that the classifier tends to absorb uncertain or overlapping examples into these broad categories.

# 

# \### E. Evidence grounding

# 

# The qualitative review also showed that retrieval can occasionally return an apparently similar historical response that does not actually address the customer's underlying problem. This makes evidence verification important rather than assuming that the top lexical match is automatically trustworthy.

# 

# \## 7. Misleading headline number

# 

# Intent accuracy alone would be a misleading headline number.

# 

# A 54% accuracy figure does not show which categories are being classified reliably, nor does it capture the operational cost of missing high-risk cases. Conversely, reporting only the 85.9% escalation recall would also be misleading because the escalation precision is 61.0%.

# 

# The more useful view combines intent performance, escalation recall/precision, retrieval quality, and evidence-grounded response evaluation. In a production support setting, the cost of an incorrect automated response to a security, financial, hardware, or data-loss issue can be much higher than the cost of escalating a routine request.

# 

# \## 8. Next week

# 

# I would prioritize the following improvements:

# 

# \- Replace heuristic weak labels with a larger reviewed training set.

# \- Refine boundaries between `unclear`, `software\_update`, and `app\_or\_feature\_issue`.

# \- Add calibrated confidence and an explicit abstention mechanism.

# \- Improve retrieval using semantic embeddings rather than lexical similarity alone.

# \- Retrieve multiple candidates and add a reranking/evidence verification step.

# \- Add multi-intent detection for messages containing multiple simultaneous problems.

# \- Incorporate conversation history instead of classifying isolated messages.

# \- Tune escalation thresholds according to business-risk costs.

# \- Expand human evaluation beyond the current 50-example qualitative sample.

# \- Increase the overlap between human and LLM evaluation so that agreement statistics are statistically meaningful.

# 

# \## 9. Decision log

# 

# 1\. Selected AppleSupport because it provided a large volume of usable support pairs.

# 2\. Reconstructed customer/support pairs using tweet-response relationships.

# 3\. Used a chronological train/test split to reduce temporal leakage.

# 4\. Defined eight operational support intents.

# 5\. Kept escalation separate from intent classification.

# 6\. Used weak supervision to create scalable baseline training labels.

# 7\. Selected TF-IDF plus Logistic Regression as an interpretable and reproducible baseline.

# 8\. Used historical support responses as retrieval evidence.

# 9\. Added explicit risk-oriented escalation rules.

# 10\. Evaluated on a fixed 200-example golden set.

# 11\. Added a separate qualitative review set for response/evidence quality.

# 12\. Reported both aggregate and per-intent metrics rather than relying on accuracy alone.

# 13\. Prioritized escalation recall because missed high-risk cases are more costly than unnecessary escalation.

# 14\. Added an LLM-as-judge evaluation for reply quality and evidence support.

# 15\. Treated the very small human/LLM overlap as an evaluation limitation rather than over-interpreting the agreement score.

