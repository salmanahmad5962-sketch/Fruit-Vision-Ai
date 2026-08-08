# ═══════════════════════════════════════════════
# FRUIT & VEGETABLE HEALTH INFORMATION DATABASE
# ═══════════════════════════════════════════════
# Reusable dictionary of health benefits, helpful conditions, vitamins,
# and warnings/precautions for every fruit/vegetable the model can detect.
# Keys are matched the same way as NUTRIENTS_DB in app.py (substring match
# on the lower-cased predicted label), so this stays in sync automatically.
#
# To add a new fruit later: just add a new "key": {...} entry below using
# the same structure. No other code changes are required.

FRUIT_HEALTH_INFO = {
    "apple": {
        "health_benefits": [
            "Supports heart health",
            "Improves digestion",
            "Boosts immunity",
            "Promotes healthy skin",
            "Rich in antioxidants",
        ],
        "helpful_for": [
            "May help support heart disease prevention",
            "Can contribute to healthy weight management",
            "Often recommended as part of a healthy diet for digestive health",
            "May help support blood sugar control",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Fiber", "benefit": "Improves digestion"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Vitamin K", "benefit": "Supports bone health"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly in moderation due to its low glycemic index.",
            "allergy": "Rare oral allergy syndrome may occur in people sensitive to birch pollen.",
            "kidney": "Safe in normal amounts for most people with kidney concerns; consult a doctor for advanced cases.",
            "other": [
                "Wash thoroughly before eating to remove pesticide residue.",
                "Apple seeds contain trace amounts of a naturally occurring toxin and should not be eaten in large quantities.",
            ],
        },
    },
    "banana": {
        "health_benefits": [
            "Boosts energy quickly",
            "Supports heart health",
            "Improves digestion",
            "Helps maintain healthy blood pressure",
            "Supports muscle function",
        ],
        "helpful_for": [
            "Often recommended as part of a healthy diet for high blood pressure",
            "May help support digestive disorders like acid reflux",
            "Can contribute to post-workout muscle recovery",
        ],
        "vitamins": [
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Vitamin B6", "benefit": "Supports brain function"},
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Fiber", "benefit": "Improves digestion"},
        ],
        "warnings": {
            "diabetes": "Should be eaten in moderation due to natural sugar content, especially when very ripe.",
            "allergy": "Rare allergy possible, sometimes linked to latex-fruit syndrome.",
            "kidney": "People with advanced kidney disease should limit intake because of high potassium content.",
            "other": ["Excess consumption may cause bloating in sensitive individuals."],
        },
    },
    "beetroot": {
        "health_benefits": [
            "Supports heart health",
            "May improve exercise performance",
            "Rich in antioxidants",
            "Supports healthy blood pressure",
            "Improves digestion",
        ],
        "helpful_for": [
            "May help support high blood pressure",
            "Can contribute to heart disease prevention",
            "Often recommended as part of a healthy diet for anemia support",
        ],
        "vitamins": [
            {"name": "Folate", "benefit": "Supports cell growth"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Fiber", "benefit": "Improves digestion"},
        ],
        "warnings": {
            "diabetes": "Can be eaten in moderation; has a moderate glycemic index.",
            "allergy": "Rare fruit/vegetable allergy may occur in sensitive individuals.",
            "kidney": "Contains oxalates, so people with kidney stones should consult a healthcare professional.",
            "other": ["May temporarily discolor urine or stool — this is harmless."],
        },
    },
    "bell pepper": {
        "health_benefits": [
            "Boosts immunity",
            "Supports eye health",
            "Rich in antioxidants",
            "Promotes healthy skin",
            "Supports heart health",
        ],
        "helpful_for": [
            "May help support eye health",
            "Often recommended as part of a healthy diet for weight management",
            "Can contribute to heart disease prevention",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Vitamin A", "benefit": "Good for vision"},
            {"name": "Vitamin B6", "benefit": "Supports brain function"},
            {"name": "Fiber", "benefit": "Improves digestion"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly because of its low glycemic index.",
            "allergy": "Rare nightshade sensitivity may occur in some individuals.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Wash thoroughly before eating.", "Remove seeds and stem before consuming."],
        },
    },
    "cabbage": {
        "health_benefits": [
            "Improves digestion",
            "Supports heart health",
            "Rich in antioxidants",
            "Boosts immunity",
            "Supports bone health",
        ],
        "helpful_for": [
            "Often recommended as part of a healthy diet for digestive disorders",
            "May help support weight management",
            "Can contribute to heart disease prevention",
        ],
        "vitamins": [
            {"name": "Vitamin K", "benefit": "Supports bone health"},
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Fiber", "benefit": "Improves digestion"},
            {"name": "Folate", "benefit": "Supports cell growth"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly because of its low glycemic index.",
            "allergy": "Rare cruciferous vegetable allergy may occur in sensitive individuals.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": [
                "Excess consumption may cause gas or digestive discomfort.",
                "People on blood thinners should keep intake consistent due to vitamin K content.",
            ],
        },
    },
    "capsicum": {
        "health_benefits": [
            "Boosts immunity",
            "Supports eye health",
            "Rich in antioxidants",
            "Promotes healthy skin",
            "Supports heart health",
        ],
        "helpful_for": [
            "May help support eye health",
            "Often recommended as part of a healthy diet for weight management",
            "Can contribute to heart disease prevention",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Vitamin A", "benefit": "Good for vision"},
            {"name": "Vitamin B6", "benefit": "Supports brain function"},
            {"name": "Fiber", "benefit": "Improves digestion"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly because of its low glycemic index.",
            "allergy": "Rare nightshade sensitivity may occur in some individuals.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Wash thoroughly before eating.", "Remove seeds and stem before consuming."],
        },
    },
    "carrot": {
        "health_benefits": [
            "Supports eye health",
            "Boosts immunity",
            "Promotes healthy skin",
            "Improves digestion",
            "Rich in antioxidants",
        ],
        "helpful_for": [
            "May help support eye health",
            "Often recommended as part of a healthy diet for weight management",
            "Can contribute to heart disease prevention",
        ],
        "vitamins": [
            {"name": "Vitamin A", "benefit": "Good for vision"},
            {"name": "Fiber", "benefit": "Improves digestion"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Vitamin K", "benefit": "Supports bone health"},
        ],
        "warnings": {
            "diabetes": "Can be eaten in moderation; cooked carrots have a higher glycemic index than raw.",
            "allergy": "Rare oral allergy syndrome may occur in people sensitive to birch pollen.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Excess consumption over long periods may cause harmless yellowing of the skin (carotenemia)."],
        },
    },
    "cauliflower": {
        "health_benefits": [
            "Improves digestion",
            "Supports heart health",
            "Boosts immunity",
            "Rich in antioxidants",
            "Supports bone health",
        ],
        "helpful_for": [
            "Often recommended as part of a healthy diet for weight management",
            "May help support digestive disorders",
            "Can contribute to heart disease prevention",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Vitamin K", "benefit": "Supports bone health"},
            {"name": "Folate", "benefit": "Supports cell growth"},
            {"name": "Fiber", "benefit": "Improves digestion"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly because of its low glycemic index.",
            "allergy": "Rare cruciferous vegetable allergy may occur in sensitive individuals.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Excess consumption may cause gas or bloating."],
        },
    },
    "corn": {
        "health_benefits": [
            "Improves digestion",
            "Supports eye health",
            "Boosts energy",
            "Rich in antioxidants",
            "Supports heart health",
        ],
        "helpful_for": [
            "May help support eye health",
            "Often recommended as part of a healthy diet for digestive health",
            "Can contribute to heart disease prevention",
        ],
        "vitamins": [
            {"name": "Fiber", "benefit": "Improves digestion"},
            {"name": "Vitamin B1", "benefit": "Supports energy metabolism"},
            {"name": "Folate", "benefit": "Supports cell growth"},
            {"name": "Potassium", "benefit": "Supports heart health"},
        ],
        "warnings": {
            "diabetes": "Should be eaten in moderation due to higher carbohydrate content.",
            "allergy": "Corn allergy is uncommon but possible in sensitive individuals.",
            "kidney": "People with advanced kidney disease should monitor potassium and phosphorus intake.",
            "other": ["Excess consumption may cause digestive discomfort in some people."],
        },
    },
    "cucumber": {
        "health_benefits": [
            "Keeps the body hydrated",
            "Supports healthy skin",
            "Improves digestion",
            "Supports heart health",
            "Low in calories",
        ],
        "helpful_for": [
            "Often recommended as part of a healthy diet for weight management",
            "May help support hydration and mild constipation relief",
            "Can contribute to healthy blood pressure",
        ],
        "vitamins": [
            {"name": "Vitamin K", "benefit": "Supports bone health"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Water content", "benefit": "Supports hydration"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly because of its very low glycemic index.",
            "allergy": "Rare fruit allergy may occur in sensitive individuals.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Wash thoroughly before eating.", "Consume in moderation if it causes bloating."],
        },
    },
    "eggplant": {
        "health_benefits": [
            "Rich in antioxidants",
            "Supports heart health",
            "Improves digestion",
            "Supports healthy blood sugar",
            "Good source of fiber",
        ],
        "helpful_for": [
            "May help support heart disease prevention",
            "Often recommended as part of a healthy diet for diabetes management",
            "Can contribute to weight management",
        ],
        "vitamins": [
            {"name": "Fiber", "benefit": "Improves digestion"},
            {"name": "Vitamin B6", "benefit": "Supports brain function"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Manganese", "benefit": "Supports bone health"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly because of its low glycemic index.",
            "allergy": "Rare nightshade sensitivity may occur in some individuals.",
            "kidney": "Contains oxalates, so people with kidney stones should consult a healthcare professional.",
            "other": ["Should be cooked before eating; raw eggplant can taste bitter.", "Remove skin if it feels tough."],
        },
    },
    "garlic": {
        "health_benefits": [
            "Boosts immunity",
            "Supports heart health",
            "Helps maintain healthy blood pressure",
            "Rich in antioxidants",
            "May support healthy cholesterol levels",
        ],
        "helpful_for": [
            "May help support high blood pressure",
            "Can contribute to heart disease prevention",
            "Often recommended as part of a healthy diet for immune support",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Vitamin B6", "benefit": "Supports brain function"},
            {"name": "Manganese", "benefit": "Supports bone health"},
            {"name": "Allicin (compound)", "benefit": "Supports cardiovascular health"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly in typical culinary amounts.",
            "allergy": "Garlic allergy or sensitivity is possible in some individuals.",
            "kidney": "Safe in normal culinary amounts for most people with kidney concerns.",
            "other": [
                "Large amounts may cause digestive discomfort or heartburn.",
                "May interact with blood-thinning medication — consult a doctor if on such medication.",
            ],
        },
    },
    "ginger": {
        "health_benefits": [
            "Improves digestion",
            "May reduce nausea",
            "Supports immunity",
            "Rich in antioxidants",
            "May help reduce inflammation",
        ],
        "helpful_for": [
            "May help support digestive disorders like nausea and bloating",
            "Often recommended as part of a healthy diet for cold and flu relief",
            "Can contribute to reducing muscle soreness",
        ],
        "vitamins": [
            {"name": "Vitamin B6", "benefit": "Supports brain function"},
            {"name": "Magnesium", "benefit": "Supports muscle function"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Gingerol (compound)", "benefit": "Provides anti-inflammatory support"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly in typical culinary amounts.",
            "allergy": "Rare allergy possible; may cause mild mouth irritation in sensitive individuals.",
            "kidney": "Safe in normal culinary amounts for most people with kidney concerns.",
            "other": ["Large amounts may cause heartburn or stomach upset.", "May interact with blood-thinning medication."],
        },
    },
    "grapes": {
        "health_benefits": [
            "Rich in antioxidants",
            "Supports heart health",
            "Boosts immunity",
            "Supports healthy skin",
            "Improves digestion",
        ],
        "helpful_for": [
            "May help support heart disease prevention",
            "Often recommended as part of a healthy diet for antioxidant intake",
            "Can contribute to healthy blood pressure",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Vitamin K", "benefit": "Supports bone health"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Resveratrol (compound)", "benefit": "Provides antioxidant support"},
        ],
        "warnings": {
            "diabetes": "Should be eaten in moderation due to natural sugar content.",
            "allergy": "Rare fruit allergy may occur in sensitive individuals.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Wash thoroughly before eating.", "Consume in moderation to avoid excess sugar intake."],
        },
    },
    "kiwi": {
        "health_benefits": [
            "Boosts immunity",
            "Improves digestion",
            "Supports heart health",
            "Rich in antioxidants",
            "Promotes healthy skin",
        ],
        "helpful_for": [
            "Often recommended as part of a healthy diet for digestive health",
            "May help support constipation",
            "Can contribute to immune support",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Vitamin K", "benefit": "Supports bone health"},
            {"name": "Fiber", "benefit": "Improves digestion"},
            {"name": "Potassium", "benefit": "Supports heart health"},
        ],
        "warnings": {
            "diabetes": "Can be eaten in moderation due to natural sugar content.",
            "allergy": "Kiwi is a known allergen for some individuals and may cause oral itching or reactions.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Skin can be eaten but is sometimes hard to digest; peeling is optional."],
        },
    },
    "lemon": {
        "health_benefits": [
            "Boosts immunity",
            "Aids digestion",
            "Supports healthy skin",
            "Rich in antioxidants",
            "Supports hydration when added to water",
        ],
        "helpful_for": [
            "Often recommended as part of a healthy diet for immune support",
            "May help support digestive health",
            "Can contribute to kidney stone prevention through citrate content",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Folate", "benefit": "Supports cell growth"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Fiber", "benefit": "Improves digestion"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly because of its low glycemic index.",
            "allergy": "Citrus allergy is rare but possible; may cause mouth or skin irritation.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Acidic juice may erode tooth enamel with excessive use.", "May irritate acid reflux in sensitive individuals."],
        },
    },
    "mango": {
        "health_benefits": [
            "Boosts immunity",
            "Supports eye health",
            "Improves digestion",
            "Promotes healthy skin",
            "Rich in antioxidants",
        ],
        "helpful_for": [
            "May help support eye health",
            "Often recommended as part of a healthy diet for digestive health",
            "Can contribute to immune support",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Vitamin A", "benefit": "Good for vision"},
            {"name": "Fiber", "benefit": "Improves digestion"},
            {"name": "Folate", "benefit": "Supports cell growth"},
        ],
        "warnings": {
            "diabetes": "Should be eaten in moderation due to relatively high natural sugar content.",
            "allergy": "Mango skin can cause contact allergy in people sensitive to poison ivy-related compounds.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Wash and peel before eating.", "Consume in moderation due to sugar content."],
        },
    },
    "onion": {
        "health_benefits": [
            "Supports heart health",
            "Boosts immunity",
            "Rich in antioxidants",
            "May support healthy blood sugar",
            "Improves digestion",
        ],
        "helpful_for": [
            "May help support heart disease prevention",
            "Often recommended as part of a healthy diet for blood sugar support",
            "Can contribute to immune support",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Vitamin B6", "benefit": "Supports brain function"},
            {"name": "Folate", "benefit": "Supports cell growth"},
            {"name": "Fiber", "benefit": "Improves digestion"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly in typical culinary amounts.",
            "allergy": "Rare allergy possible; may cause mild irritation in sensitive individuals.",
            "kidney": "Safe in normal culinary amounts for most people with kidney concerns.",
            "other": ["Raw onion may cause digestive discomfort or heartburn in some people."],
        },
    },
    "orange": {
        "health_benefits": [
            "Boosts immunity",
            "Supports heart health",
            "Improves digestion",
            "Promotes healthy skin",
            "Rich in antioxidants",
        ],
        "helpful_for": [
            "Often recommended as part of a healthy diet for immune support",
            "May help support heart disease prevention",
            "Can contribute to healthy digestion",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Folate", "benefit": "Supports cell growth"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Fiber", "benefit": "Improves digestion"},
        ],
        "warnings": {
            "diabetes": "Can be eaten in moderation due to natural sugar content; whole fruit is preferred over juice.",
            "allergy": "Citrus allergy is rare but possible.",
            "kidney": "People with advanced kidney disease should monitor potassium intake.",
            "other": ["May irritate acid reflux in sensitive individuals."],
        },
    },
    "pear": {
        "health_benefits": [
            "Improves digestion",
            "Supports heart health",
            "Boosts immunity",
            "Supports healthy blood sugar",
            "Rich in antioxidants",
        ],
        "helpful_for": [
            "Often recommended as part of a healthy diet for digestive health",
            "May help support constipation",
            "Can contribute to heart disease prevention",
        ],
        "vitamins": [
            {"name": "Fiber", "benefit": "Improves digestion"},
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Vitamin K", "benefit": "Supports bone health"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly because of its low glycemic index.",
            "allergy": "Rare oral allergy syndrome may occur in people sensitive to birch pollen.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Wash thoroughly before eating.", "Remove seeds before eating."],
        },
    },
    "pineapple": {
        "health_benefits": [
            "Boosts immunity",
            "Improves digestion",
            "Rich in antioxidants",
            "Supports bone health",
            "May help reduce inflammation",
        ],
        "helpful_for": [
            "Often recommended as part of a healthy diet for digestive health",
            "May help support inflammation-related discomfort",
            "Can contribute to immune support",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Manganese", "benefit": "Supports bone health"},
            {"name": "Bromelain (enzyme)", "benefit": "Supports digestion"},
            {"name": "Fiber", "benefit": "Improves digestion"},
        ],
        "warnings": {
            "diabetes": "Should be eaten in moderation due to natural sugar content.",
            "allergy": "Pineapple can cause mouth or tongue irritation due to bromelain in some individuals.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Remove the tough core and skin before eating.", "Excess consumption may cause mouth soreness."],
        },
    },
    "pomegranate": {
        "health_benefits": [
            "Rich in antioxidants",
            "Supports heart health",
            "Boosts immunity",
            "Helps maintain healthy blood pressure",
            "Improves digestion",
        ],
        "helpful_for": [
            "May help support heart disease prevention",
            "Often recommended as part of a healthy diet for high blood pressure",
            "Can contribute to healthy digestion",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Vitamin K", "benefit": "Supports bone health"},
            {"name": "Folate", "benefit": "Supports cell growth"},
            {"name": "Fiber", "benefit": "Improves digestion"},
        ],
        "warnings": {
            "diabetes": "Can be eaten in moderation due to natural sugar content.",
            "allergy": "Rare fruit allergy may occur in sensitive individuals.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Remove seeds' hard casing if it causes digestive discomfort.", "Consume in moderation."],
        },
    },
    "potato": {
        "health_benefits": [
            "Boosts energy",
            "Supports heart health",
            "Improves digestion",
            "Rich in antioxidants",
            "Good source of potassium",
        ],
        "helpful_for": [
            "Often recommended as part of a healthy diet for energy needs",
            "May help support healthy blood pressure",
            "Can contribute to muscle function support",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Vitamin B6", "benefit": "Supports brain function"},
            {"name": "Fiber", "benefit": "Improves digestion (with skin)"},
        ],
        "warnings": {
            "diabetes": "Should be eaten in moderation due to higher glycemic index, especially when fried or mashed.",
            "allergy": "Rare nightshade sensitivity may occur in some individuals.",
            "kidney": "People with advanced kidney disease should monitor potassium intake.",
            "other": ["Avoid eating green or sprouted potatoes, as they contain natural toxins.", "Cook thoroughly before eating."],
        },
    },
    "strawberry": {
        "health_benefits": [
            "Boosts immunity",
            "Supports heart health",
            "Rich in antioxidants",
            "Promotes healthy skin",
            "Improves digestion",
        ],
        "helpful_for": [
            "Often recommended as part of a healthy diet for immune support",
            "May help support heart disease prevention",
            "Can contribute to healthy blood sugar levels",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Manganese", "benefit": "Supports bone health"},
            {"name": "Folate", "benefit": "Supports cell growth"},
            {"name": "Fiber", "benefit": "Improves digestion"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly because of its low glycemic index.",
            "allergy": "Strawberries are a known allergen for some individuals and may cause itching or hives.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Wash thoroughly before eating.", "Remove the green cap/stem before consuming."],
        },
    },
    "tomato": {
        "health_benefits": [
            "Supports heart health",
            "Rich in antioxidants",
            "Supports eye health",
            "Promotes healthy skin",
            "Improves digestion",
        ],
        "helpful_for": [
            "May help support heart disease prevention",
            "Often recommended as part of a healthy diet for eye health",
            "Can contribute to healthy blood pressure",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Vitamin K", "benefit": "Supports bone health"},
            {"name": "Lycopene (compound)", "benefit": "Provides antioxidant support"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly because of its low glycemic index.",
            "allergy": "Rare nightshade sensitivity may occur in some individuals.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["May worsen acid reflux in sensitive individuals.", "Wash thoroughly before eating."],
        },
    },
    "watermelon": {
        "health_benefits": [
            "Keeps the body hydrated",
            "Supports heart health",
            "Rich in antioxidants",
            "Supports healthy skin",
            "Low in calories",
        ],
        "helpful_for": [
            "May help support hydration",
            "Often recommended as part of a healthy diet for weight management",
            "Can contribute to heart disease prevention",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Vitamin A", "benefit": "Good for vision"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Lycopene (compound)", "benefit": "Provides antioxidant support"},
        ],
        "warnings": {
            "diabetes": "Should be eaten in moderation due to relatively high natural sugar content.",
            "allergy": "Rare fruit allergy may occur in sensitive individuals.",
            "kidney": "People with advanced kidney disease should monitor potassium intake.",
            "other": ["Excess consumption may cause bloating due to high water and fiber content."],
        },
    },
    "peach": {
        "health_benefits": [
            "Boosts immunity",
            "Improves digestion",
            "Supports eye health",
            "Promotes healthy skin",
            "Rich in antioxidants",
        ],
        "helpful_for": [
            "Often recommended as part of a healthy diet for digestive health",
            "May help support eye health",
            "Can contribute to immune support",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Vitamin A", "benefit": "Good for vision"},
            {"name": "Fiber", "benefit": "Improves digestion"},
            {"name": "Potassium", "benefit": "Supports heart health"},
        ],
        "warnings": {
            "diabetes": "Can be eaten in moderation due to natural sugar content.",
            "allergy": "Peach fuzz/skin can cause oral allergy syndrome in people sensitive to birch pollen.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Wash thoroughly before eating.", "Remove the pit before consuming."],
        },
    },
    "cherry": {
        "health_benefits": [
            "Rich in antioxidants",
            "Supports heart health",
            "May improve sleep quality",
            "May help reduce inflammation",
            "Boosts immunity",
        ],
        "helpful_for": [
            "May help support heart disease prevention",
            "Often recommended as part of a healthy diet for inflammation-related discomfort",
            "Can contribute to better sleep quality",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Fiber", "benefit": "Improves digestion"},
            {"name": "Melatonin (compound)", "benefit": "Supports sleep quality"},
        ],
        "warnings": {
            "diabetes": "Should be eaten in moderation due to natural sugar content.",
            "allergy": "Rare oral allergy syndrome may occur in people sensitive to birch pollen.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Remove the pit before eating — it is not edible and contains natural toxins."],
        },
    },
    "plum": {
        "health_benefits": [
            "Improves digestion",
            "Supports heart health",
            "Boosts immunity",
            "Rich in antioxidants",
            "May support healthy bones",
        ],
        "helpful_for": [
            "Often recommended as part of a healthy diet for constipation",
            "May help support digestive disorders",
            "Can contribute to heart disease prevention",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Vitamin K", "benefit": "Supports bone health"},
            {"name": "Fiber", "benefit": "Improves digestion"},
            {"name": "Potassium", "benefit": "Supports heart health"},
        ],
        "warnings": {
            "diabetes": "Can be eaten in moderation due to natural sugar content.",
            "allergy": "Rare oral allergy syndrome may occur in people sensitive to birch pollen.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Remove the pit before eating.", "Excess consumption may have a laxative effect."],
        },
    },
    "coconut": {
        "health_benefits": [
            "Provides quick energy",
            "Supports hydration (coconut water)",
            "Supports healthy hair and skin",
            "Contains beneficial fatty acids",
            "Improves digestion",
        ],
        "helpful_for": [
            "May help support hydration and electrolyte balance",
            "Often recommended as part of a healthy diet in moderate amounts for energy",
            "Can contribute to skin and hair health",
        ],
        "vitamins": [
            {"name": "Manganese", "benefit": "Supports bone health"},
            {"name": "Fiber", "benefit": "Improves digestion"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Medium-chain triglycerides", "benefit": "Provides quick-use energy"},
        ],
        "warnings": {
            "diabetes": "Can be eaten in moderation; naturally low in sugar but high in saturated fat.",
            "allergy": "Coconut allergy is uncommon but possible, sometimes linked to tree nut allergies.",
            "kidney": "People with advanced kidney disease should monitor potassium intake, especially from coconut water.",
            "other": ["High in saturated fat — consume in moderation as part of a balanced diet."],
        },
    },
    "lime": {
        "health_benefits": [
            "Boosts immunity",
            "Aids digestion",
            "Supports healthy skin",
            "Rich in antioxidants",
            "Supports hydration when added to water",
        ],
        "helpful_for": [
            "Often recommended as part of a healthy diet for immune support",
            "May help support digestive health",
            "Can contribute to kidney stone prevention through citrate content",
        ],
        "vitamins": [
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Folate", "benefit": "Supports cell growth"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Fiber", "benefit": "Improves digestion"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly because of its low glycemic index.",
            "allergy": "Citrus allergy is rare but possible; may cause mouth or skin irritation.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Acidic juice may erode tooth enamel with excessive use.", "May irritate acid reflux in sensitive individuals."],
        },
    },
    "avocado": {
        "health_benefits": [
            "Supports heart health",
            "Contains beneficial fatty acids",
            "Improves digestion",
            "Supports healthy skin",
            "Rich in antioxidants",
        ],
        "helpful_for": [
            "May help support heart disease prevention",
            "Often recommended as part of a healthy diet for healthy cholesterol levels",
            "Can contribute to weight management as part of a balanced diet",
        ],
        "vitamins": [
            {"name": "Vitamin K", "benefit": "Supports bone health"},
            {"name": "Fiber", "benefit": "Improves digestion"},
            {"name": "Potassium", "benefit": "Supports heart health"},
            {"name": "Folate", "benefit": "Supports cell growth"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly because of its low sugar and low glycemic index.",
            "allergy": "Avocado allergy is possible, sometimes linked to latex-fruit syndrome.",
            "kidney": "People with advanced kidney disease should monitor potassium intake.",
            "other": ["High in calories and fat — consume in moderation as part of a balanced diet."],
        },
    },
    "pumpkin": {
        "health_benefits": [
            "Supports eye health",
            "Boosts immunity",
            "Rich in antioxidants",
            "Improves digestion",
            "Supports healthy skin",
        ],
        "helpful_for": [
            "May help support eye health",
            "Often recommended as part of a healthy diet for weight management",
            "Can contribute to healthy digestion",
        ],
        "vitamins": [
            {"name": "Vitamin A", "benefit": "Good for vision"},
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Fiber", "benefit": "Improves digestion"},
            {"name": "Potassium", "benefit": "Supports heart health"},
        ],
        "warnings": {
            "diabetes": "Can be eaten in moderation; has a moderate-to-high glycemic index when cooked.",
            "allergy": "Rare fruit/vegetable allergy may occur in sensitive individuals.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": ["Seeds should be removed or roasted separately before eating the flesh."],
        },
    },
    "broccoli": {
        "health_benefits": [
            "Boosts immunity",
            "Supports bone health",
            "Rich in antioxidants",
            "Improves digestion",
            "Supports heart health",
        ],
        "helpful_for": [
            "Often recommended as part of a healthy diet for bone health",
            "May help support heart disease prevention",
            "Can contribute to weight management",
        ],
        "vitamins": [
            {"name": "Vitamin K", "benefit": "Supports bone health"},
            {"name": "Vitamin C", "benefit": "Supports immunity"},
            {"name": "Fiber", "benefit": "Improves digestion"},
            {"name": "Folate", "benefit": "Supports cell growth"},
        ],
        "warnings": {
            "diabetes": "Generally diabetes-friendly because of its low glycemic index.",
            "allergy": "Rare cruciferous vegetable allergy may occur in sensitive individuals.",
            "kidney": "Safe in normal amounts for most people with kidney concerns.",
            "other": [
                "Excess consumption may cause gas or bloating.",
                "People on blood thinners should keep intake consistent due to vitamin K content.",
            ],
        },
    },
}

_NOT_AVAILABLE = "Information not available for this fruit."

DEFAULT_HEALTH_INFO = {
    "health_benefits": [_NOT_AVAILABLE],
    "helpful_for": [_NOT_AVAILABLE],
    "vitamins": [],
    "warnings": {
        "diabetes": _NOT_AVAILABLE,
        "allergy": _NOT_AVAILABLE,
        "kidney": _NOT_AVAILABLE,
        "other": [_NOT_AVAILABLE],
    },
}


def get_health_info(label: str) -> dict:
    """Look up health info for a predicted label using the same substring
    matching strategy as resolve_nutrients() in app.py, so results stay
    consistent with the nutrition data for the same fruit."""
    lower = (label or "").lower().replace("_", " ")
    for key, value in FRUIT_HEALTH_INFO.items():
        if key in lower:
            return value
    return DEFAULT_HEALTH_INFO
