# \# Hiver SDE Intern — Take-Home Assignment Report

# 

# \## 1. Problem Framing

# 

# \### Objective

# 

# I built a lightweight AI support copilot for AppleSupport using the Customer Support on Twitter dataset.

# 

# For each incoming customer message, the system performs four tasks:

# 

# 1\. Classifies the message into one of eight support intents.

# 2\. Retrieves historically similar AppleSupport conversations.

# 3\. Drafts a reply grounded in those historical resolutions.

# 4\. Decides whether the interaction can be auto-handled or should be escalated to a human, with a stated reason.

# 

# For this brand, I define a good system as one that is useful for routine support while being conservative around higher-risk cases. A response should be relevant to the customer's issue, grounded in historical support behavior, and avoid confidently giving an unsupported answer.

# 

# I deliberately did not build a fully autonomous production support agent. The system does not attempt payments, account changes, device diagnostics, or other irreversible actions. Escalation is treated as a separate safety layer rather than assuming that every confidently classified message should be automatically handled.

# 

# \---

# 

# \## 2. Data and Intent Taxonomy

# 

# \### Dataset

# 

# I used the Kaggle Customer Support on Twitter dataset (`thoughtvector/customer-support-on-twitter`). The dataset contains customer-to-brand and brand-to-customer tweets, with response identifiers that can be used to reconstruct support interactions.

# 

# I selected \*\*AppleSupport\*\* because it provided a large number of usable customer/support pairs and broad coverage of common technical-support scenarios.

# 

# After pairing customer messages with their corresponding AppleSupport responses, the selected brand provided approximately \*\*106,623 usable pairs\*\*, with approximately \*\*99.8% pairing coverage\*\* among the AppleSupport responses considered.

# 

# The data was split chronologically to reduce leakage from future conversations into training.

# 

# The working split contained approximately:

# 

# \- Training: 85,298 examples

# \- Test: 21,325 examples

# \- Golden evaluation set: 200 examples

# 

# \### Intent taxonomy

# 

# I defined eight intents based on recurring support patterns in the AppleSupport data:

# 

# \- `software\_update` — Problems installing, updating, restoring, or reverting an OS update, including problems directly caused by an iOS/macOS update.

# \- `device\_performance` — General device instability, performance problems, crashing, freezing, unexpected restarting, overheating, shutdowns, and similar device-level problems.

# \- `app\_or\_feature\_issue` — A specific Apple app, feature, or functionality is malfunctioning or behaving unexpectedly.

# \- `connectivity` — Wi-Fi, Bluetooth, cellular, phone-call, network, or connection problems.

# \- `account\_security` — Account access, authentication, suspicious communications, phishing, security issues, or locked-out device/account situations.

# \- `purchase\_repair\_support` — Purchases, trade-ins, repairs, replacements, damaged hardware, store support, or service.

# \- `information\_request` — Primarily informational questions such as compatibility, feature explanations, or how-to requests without a specific malfunction.

# \- `unclear` — Not enough information to confidently determine the customer's intent.

# 

# Escalation is deliberately modeled separately from intent because the same intent can contain both routine and high-risk cases.

# 

# \---

# 

# \## 3. System Design

# 

# \### Intent classification

# 

# The main classifier uses word- and character-level TF-IDF features with balanced Logistic Regression.

# 

# This provides a simple, fast baseline model that is easy to inspect and reproduce. The model outputs an intent prediction that is then passed to the retrieval and escalation stages.

# 

# \### Historical retrieval and reply drafting

# 

# For each customer message, the system retrieves historically similar AppleSupport customer/support examples.

# 

# The retrieved support response is used as grounding evidence for the draft reply. This keeps the system tied to actual historical resolutions rather than generating an answer entirely from model knowledge.

# 

# The evaluation records the retrieval similarity score so that grounding quality can be inspected independently of intent classification.

# 

# \### Escalation

# 

# A separate rule-based escalation layer identifies higher-risk situations.

# 

# Signals include:

# 

# \- Physical or device damage.

# \- Financial or purchase-related risk.

# \- Account/security concerns.

# \- Repair or replacement requirements.

# \- Insufficient information.

# \- Potential data loss.

# \- Severe device instability.

# 

# Routine informational or troubleshooting requests are more likely to be auto-handled.

# 

# This separation is intentional: a correct intent classification does not automatically mean that autonomous handling is safe.

# 

# \---

# 

# \## 4. Evaluation

# 

# \### Golden evaluation set

# 

# I created a 200-example golden evaluation set sampled from the AppleSupport data.

# 

# The examples were reviewed and curated for intent and escalation labels, with annotation notes recorded alongside the labels. The set covers all eight intent categories and is used consistently across the evaluation harness.

# 

# The labels were reviewed during the take-home process. Because the initial candidate labels were generated with heuristic/model assistance before review, I treat these as \*\*reviewed golden labels rather than independently double-annotated human labels\*\*.

# 

# \### Main results

# 

# On the 200-example golden set:

# 

# | Metric | Result |

# |---|---:|

# | Intent accuracy | \*\*54.0%\*\* |

# | Escalation precision | \*\*61.0%\*\* |

# | Escalation recall | \*\*85.9%\*\* |

# | Escalation F1 | \*\*71.3%\*\* |

# | Average retrieval similarity | \*\*0.344\*\* |

# | Average draft reply length | \*\*262.7 characters\*\* |

# 

# The escalation layer intentionally favors recall because missing a risky case is more costly than escalating an otherwise routine request.

# 

# \### Intent-level results

# 

# | Intent | Precision | Recall | F1 |

# |---|---:|---:|---:|

# | account\_security | 0.80 | 0.63 | 0.71 |

# | app\_or\_feature\_issue | 0.94 | 0.37 | 0.53 |

# | connectivity | 0.67 | 0.86 | 0.75 |

# | device\_performance | 0.81 | 0.46 | 0.59 |

# | information\_request | 0.88 | 0.30 | 0.45 |

# | purchase\_repair\_support | 0.75 | 0.32 | 0.44 |

# | software\_update | 0.46 | 0.92 | 0.61 |

# | unclear | 0.31 | 0.77 | 0.44 |

# 

# The model performs particularly well on connectivity and account/security precision, while software-update and unclear cases show substantial overlap with other categories.

# 

# \---

# 

# \## 5. Results vs. Baselines

# 

# I evaluated the main classifier against two baselines on the same 200-example golden set.

# 

# \### Baseline 1: Majority-class classifier

# 

# The trivial baseline always predicts the most common intent in the golden set.

# 

# The most common class was `app\_or\_feature\_issue`.

# 

# This baseline achieved:

# 

# \*\*20.5% intent accuracy.\*\*

# 

# \### Baseline 2: Keyword/rule classifier

# 

# The simple baseline uses deterministic keyword rules for the eight intent categories. For example, terms associated with Wi-Fi/network problems map to `connectivity`, update-related terms map to `software\_update`, and repair/replacement terms map to `purchase\_repair\_support`.

# 

# This baseline achieved:

# 

# \*\*45.0% intent accuracy.\*\*

# 

# \### Comparison

# 

# | Approach | Intent Accuracy |

# |---|---:|

# | Majority-class baseline | \*\*20.5%\*\* |

# | Keyword/rule baseline | \*\*45.0%\*\* |

# | TF-IDF + Logistic Regression | \*\*54.0%\*\* |

# 

# The learned model improves accuracy by \*\*33.5 percentage points over the majority baseline\*\* and \*\*9.0 percentage points over the keyword baseline\*\*.

# 

# This indicates that the learned model adds measurable value beyond both a trivial predictor and a manually constructed heuristic system.

# 

# However, the remaining 46% error rate shows that the classifier is not yet reliable enough to be treated as a standalone production decision-maker.

# 

# \---

# 

# \## 6. Reply Quality and LLM-as-Judge

# 

# I added an LLM-based evaluation stage to assess generated replies on four dimensions:

# 

# 1\. Helpfulness.

# 2\. Correctness.

# 3\. Clarity.

# 4\. Whether the reply is supported by the retrieved evidence.

# 

# The judge evaluated \*\*200 examples\*\* using Gemini through its OpenAI-compatible API.

# 

# A separate 50-example qualitative review sample was also created with fields for evidence support, helpfulness, correctness, clarity, and notes.

# 

# \### Human/LLM agreement

# 

# The evaluation harness compares the human-reviewed and LLM-judged labels using Cohen's kappa.

# 

# The resulting file reports:

# 

# \- Agreement examples: \*\*3\*\*

# \- Cohen's kappa: \*\*0.00\*\*

# 

# This should \*\*not\*\* be interpreted as strong evidence that the judge is poor or good. Only three examples contained valid overlapping labels from both sources, which is far too small a sample for a reliable agreement estimate.

# 

# The appropriate conclusion is that the current agreement measurement is inconclusive and that a larger independently human-reviewed overlap set is needed before relying heavily on the LLM judge.

# 

# \---

# 

# \## 7. Failure Analysis

# 

# \### 1. Short or ambiguous customer messages

# 

# Many tweets are extremely short, such as messages that mention only a symptom or a product feature without explaining the actual problem.

# 

# These examples can reasonably belong to multiple intents.

# 

# \*\*Hypothesis:\*\* The classifier needs either conversation context or an explicit uncertainty/abstention mechanism.

# 

# \### 2. Software-update overlap

# 

# Update-related words occur in messages where the underlying issue is actually device performance or an app/feature problem.

# 

# The model therefore tends to overpredict `software\_update`.

# 

# \*\*Hypothesis:\*\* The taxonomy needs clearer priority rules and examples distinguishing "the update itself is failing" from "something broke after an update."

# 

# \### 3. `unclear` overprediction

# 

# The `unclear` class has relatively high recall but low precision.

# 

# Short messages, missing context, and multi-symptom tweets make the class difficult to define consistently.

# 

# \*\*Hypothesis:\*\* Some examples currently labeled `unclear` would benefit from a confidence threshold and an explicit "needs more information" action instead of forcing a semantic intent.

# 

# \### 4. Retrieval mismatch

# 

# A retrieved historical response can be lexically similar while addressing a different underlying problem.

# 

# For example, two tweets may mention the same Apple feature but require different troubleshooting steps.

# 

# \*\*Hypothesis:\*\* TF-IDF similarity is useful as a first retrieval stage but is not sufficient as the final evidence-selection mechanism.

# 

# \### 5. Unsupported or weakly grounded replies

# 

# If retrieval selects a poor historical example, the generated response can inherit that mismatch.

# 

# This is particularly risky when the message concerns security, account access, hardware damage, or data loss.

# 

# \*\*Hypothesis:\*\* Reply generation should require an evidence-quality threshold and abstain/escalate when no sufficiently relevant historical resolution is retrieved.

# 

# \---

# 

# \## 8. What Is Misleading About My Headline Number?

# 

# The headline intent accuracy is \*\*54.0%\*\*, but presenting only that number would be misleading.

# 

# First, accuracy hides the large differences between intent classes. For example, connectivity has much stronger recall than information requests, while software updates are frequently predicted even when they are not the correct underlying intent.

# 

# Second, intent accuracy does not measure whether a generated reply is safe or useful.

# 

# Third, escalation has a different risk profile. An escalation recall of \*\*85.9%\*\* sounds strong, but the corresponding precision is only \*\*61.0%\*\*, meaning that a substantial number of escalations are unnecessary.

# 

# Therefore, the system should not be described as "54% accurate" and considered production-ready. The more useful view is a collection of measurements covering classification, escalation, retrieval grounding, and reply quality.

# 

# \---

# 

# \## 9. What I Would Do With One More Week

# 

# \### 1. Improve annotation quality

# 

# Create a larger independently human-reviewed evaluation set and double-label a subset to measure inter-annotator agreement.

# 

# \### 2. Refine taxonomy boundaries

# 

# Review confusion between `software\_update`, `device\_performance`, `app\_or\_feature\_issue`, and `unclear`.

# 

# \### 3. Add calibrated confidence and abstention

# 

# Instead of forcing every message into an intent, use confidence thresholds and route ambiguous messages for clarification or human review.

# 

# \### 4. Use semantic retrieval

# 

# Replace or augment TF-IDF retrieval with sentence embeddings to better capture semantic similarity.

# 

# \### 5. Add reranking and evidence verification

# 

# Retrieve multiple candidate historical resolutions, rerank them, and require the final evidence to meet a relevance threshold before generating a reply.

# 

# \### 6. Use conversation history

# 

# A single tweet often lacks enough context. Reconstructing more of the conversation thread should improve both classification and retrieval.

# 

# \### 7. Support multi-intent messages

# 

# Some customers describe several problems in one message. The system should identify the primary issue and preserve secondary issues rather than forcing everything into one label.

# 

# \### 8. Improve escalation calibration

# 

# Tune escalation thresholds according to business risk rather than optimizing a single generic metric.

# 

# \### 9. Expand reply evaluation

# 

# Increase the independently human-reviewed overlap with the LLM judge so that judge agreement can be measured reliably.

# 

# \### 10. Add safety-oriented reply constraints

# 

# For security, financial, account-access, hardware-damage, and data-loss scenarios, prefer clarification or escalation over speculative troubleshooting.

# 

# \---

# 

# \## 10. Decision Log

# 

# 1\. \*\*Selected AppleSupport\*\* because it had a large number of usable customer/support pairs and broad support coverage.

# 2\. \*\*Used response IDs to construct customer/support pairs\*\* rather than treating isolated tweets as independent examples.

# 3\. \*\*Used a chronological split\*\* to reduce temporal leakage between training and evaluation.

# 4\. \*\*Defined eight intents\*\* to balance useful routing with a manageable taxonomy.

# 5\. \*\*Kept escalation separate from intent\*\* because the same intent can contain both safe and risky cases.

# 6\. \*\*Included `unclear`\*\* rather than forcing ambiguous messages into a potentially incorrect support category.

# 7\. \*\*Used TF-IDF + Logistic Regression\*\* because it is fast, reproducible, interpretable, and appropriate as a strong lightweight baseline.

# 8\. \*\*Used both word and character features\*\* to handle natural-language variation and noisy social-media text.

# 9\. \*\*Used historical-response retrieval\*\* so that replies are grounded in the selected brand's observed support behavior.

# 10\. \*\*Made escalation conservative\*\* around security, financial, repair, damage, and data-loss signals.

# 11\. \*\*Evaluated against a majority baseline\*\* to establish a trivial lower bound.

# 12\. \*\*Evaluated against a keyword baseline\*\* to determine whether the learned model improves over simple human-written heuristics.

# 13\. \*\*Used a fixed 200-example golden set\*\* for repeatable comparison across pipeline changes.

# 14\. \*\*Added an LLM judge\*\* to evaluate reply quality beyond classification metrics.

# 15\. \*\*Reported the human/LLM agreement limitation explicitly\*\* rather than treating a three-example overlap as statistically meaningful.

# 

# \---

# 

# \## 11. Conclusion

# 

# The resulting system is a working prototype rather than a production-ready autonomous support agent.

# 

# The main classifier reaches \*\*54.0% accuracy\*\*, substantially outperforming both the \*\*20.5% majority baseline\*\* and the \*\*45.0% keyword baseline\*\*. The escalation layer achieves \*\*85.9% recall\*\* with \*\*61.0% precision\*\*, reflecting the deliberate choice to prioritize catching potentially risky cases.

# 

# The most important limitation is that noisy, short, and multi-intent support messages make intent boundaries difficult, while lexical retrieval can select superficially similar but operationally different historical resolutions.

# 

# The next stage should therefore focus less on adding complexity and more on improving annotation quality, semantic retrieval, confidence-based abstention, conversation context, and independently human-validated reply evaluation.

