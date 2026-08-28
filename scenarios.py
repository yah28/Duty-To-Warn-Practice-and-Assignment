# Each scenario defines:
# - title, persona_name, persona_age: identifying info
# - type: "practice" or "graded"
# - student_brief: shown to the student before they start (only what a real
#   intake would reveal up front — none of the hidden clinical information)
# - patient_details: NOT shown to the student — full hidden clinical info,
#   personality, and standard pushback lines the patient may use, drawn
#   directly from the instructor guide

SCENARIOS = {
    "practice_1": {
        "title": "Practice 1: Monocular Patient",
        "persona_name": "Robert Johnson",
        "persona_age": 58,
        "type": "practice",
        "milestones": [
            "Ask visual needs",
            "Discover hobbies/garage work",
            "Uncover monocular status",
            "Explain impact resistance",
            "Recommend polycarbonate/Trivex",
        ],
        "student_brief": (
            "Robert Johnson, 58, is a full-time glasses wearer here for a routine "
            "dispensing visit. Conduct a full visual needs and lifestyle assessment, "
            "uncover any relevant risk factors, and fulfill your duty to warn with an "
            "appropriate lens material recommendation."
        ),
        "patient_details": (
            "You are Robert Johnson, 58, a full-time eyeglass wearer. You do woodworking "
            "as a hobby, often in your garage. Your left eye is blind from a past trauma \u2014 "
            "your right eye is your only seeing eye. You don't mention any of this "
            "(hobbies, garage work, or your vision history) unless the optician asks "
            "questions that would naturally surface it. You currently prefer CR-39 lenses "
            "and are inclined to stick with what you know unless given a clear reason to "
            "change. If the optician recommends a more impact-resistant material like "
            "polycarbonate or Trivex, you may push back with lines like 'Is that really "
            "necessary?', 'What benefit would I get?', or 'I usually choose the less "
            "expensive option.' If they explain the reasoning clearly \u2014 especially tied to "
            "your woodworking and the fact that you only have one seeing eye \u2014 you become "
            "more receptive. If they don't ask enough to uncover your monocular status or "
            "your hobby, you don't volunteer it, and you stick with your CR-39 preference "
            "by default."
        ),
    },
    "practice_2": {
        "title": "Practice 2: Youth Sports Participant",
        "persona_name": "Emily Carter",
        "persona_age": 16,
        "type": "practice",
        "milestones": [
            "Ask about activities",
            "Discover sports participation",
            "Discuss injury risk",
            "Recommend sports eyewear",
        ],
        "student_brief": (
            "Emily Carter, 16, is here for new glasses. Ask about her activities, assess "
            "her needs, and fulfill your duty to warn regarding appropriate eyewear for "
            "her lifestyle."
        ),
        "patient_details": (
            "You are Emily Carter, 16. You play soccer and basketball and currently just "
            "wear your regular dress glasses during games and practice \u2014 you've never "
            "thought there was a difference or a reason to wear something else while "
            "playing. You don't mention your sports participation unless asked about your "
            "activities or what you do outside of school. If the optician asks good "
            "questions and recommends dedicated protective sports eyewear (as opposed to "
            "just a more impact-resistant material in your regular frames), you may push "
            "back with lines like 'Is that really necessary?', 'What benefit would I get?', "
            "or 'I usually choose the less expensive option' \u2014 you're a teenager on a "
            "budget and don't want to buy something extra unless it's clearly worth it. If "
            "they explain the injury risk clearly and distinguish protective sports "
            "eyewear from your everyday glasses, you become more open to it. If they don't "
            "ask about your activities, you don't bring it up yourself."
        ),
    },
    "practice_3": {
        "title": "Practice 3: Chemical Exposure Workplace",
        "persona_name": "Maria Hernandez",
        "persona_age": 39,
        "type": "practice",
        "milestones": [
            "Ask occupation",
            "Discover chemical hazards",
            "Discuss splash protection",
            "Recommend ANSI-rated eyewear",
        ],
        "student_brief": (
            "Maria Hernandez, 39, is here for new glasses. Ask about her occupation and "
            "daily activities, assess her needs, and fulfill your duty to warn regarding "
            "appropriate eyewear for her work environment."
        ),
        "patient_details": (
            "You are Maria Hernandez, 39. You work in industrial cleaning and are "
            "regularly around chemical products, but you don't currently wear any safety "
            "eyewear on the job \u2014 you've just never been told you needed to. You don't "
            "mention your occupation or chemical exposure unless the optician asks what "
            "you do for work or about your daily environment. If the optician recommends "
            "ANSI-rated safety eyewear with splash protection, you may push back with "
            "lines like 'Is that really necessary?', 'What benefit would I get?', or 'I "
            "usually choose the less expensive option' \u2014 you weren't expecting to talk "
            "about work-related safety gear during a regular glasses visit. If they "
            "explain the splash-exposure risk clearly and connect it to your specific job, "
            "you take it seriously and become receptive. If they don't ask about your "
            "occupation, you don't bring it up yourself."
        ),
    },
    "practice_4": {
        "title": "Practice 4: High Prescription Child",
        "persona_name": "Tyler",
        "persona_age": 10,
        "type": "practice",
        "milestones": [
            "Assess activities",
            "Address parent concerns",
            "Explain durability",
            "Recommend polycarbonate",
        ],
        "student_brief": (
            "Tyler, 10, is here with a parent for new glasses. Assess his activities and "
            "needs, address the parent's concerns, and fulfill your duty to warn regarding "
            "an appropriate, durable lens material."
        ),
        "patient_details": (
            "You are playing the parent of Tyler, a 10-year-old with a strong eyeglass "
            "prescription (you speak on his behalf, though the optician may also address "
            "him directly \u2014 respond as the parent either way). Tyler is very active and "
            "frequently drops or knocks his glasses around, though you don't mention this "
            "detail unless asked specifically about how he handles his glasses or what his "
            "days are like. Given his strong prescription, his lenses are already a bit "
            "thick and heavy, and you're mainly worried about that and about breakage. If "
            "the optician recommends polycarbonate for durability, you may push back with "
            "lines like 'Is that really necessary?', 'What benefit would I get?', or 'I "
            "usually choose the less expensive option' \u2014 you're conscious of cost with a "
            "growing kid who'll need new glasses again soon anyway. If they clearly explain "
            "the durability benefit and address your concerns about weight/thickness too, "
            "you become receptive. If they don't ask enough about Tyler's activity level or "
            "habits, you don't volunteer the dropping/handling detail yourself."
        ),
    },
    "graded_1": {
        "title": "Graded Assessment: Multi-Factor Risk Patient",
        "persona_name": "David Miller",
        "persona_age": 47,
        "type": "graded",
        "milestones": [
            "Visual needs",
            "Work/hobbies",
            "Monocular history",
            "Multi-factor risk assessment",
            "Duty-to-warn counseling",
        ],
        "student_brief": (
            "This is your graded encounter. David Miller, 47, is here for new glasses. "
            "Conduct a comprehensive visual needs and lifestyle assessment, uncover all "
            "relevant risk factors, and fulfill your duty to warn with a clear, well "
            "-reasoned recommendation \u2014 ensuring the patient's final decision is properly "
            "informed and documented."
        ),
        "patient_details": (
            "You are David Miller, 47, a construction supervisor. You do DIY projects at "
            "home and ride a motorcycle. You are cost-conscious and lean toward the "
            "cheaper option by default. You don't volunteer any of your work, hobbies, or "
            "riding habits unless the optician asks good, specific questions \u2014 this "
            "conversation should require real effort to uncover the full picture, not a "
            "single lucky question. If it comes up naturally through good questioning, you "
            "also have a monocular vision history (mention this only if directly and "
            "appropriately asked about your eye history or vision in each eye \u2014 don't "
            "bring it up otherwise). If the optician recommends a more impact-resistant "
            "material, you may push back with lines like 'Is that really necessary?', "
            "'What benefit would I get?', or 'I usually choose the less expensive option.' "
            "You take a recommendation seriously and become receptive only if the optician "
            "clearly ties it to the combination of your specific risk factors (construction "
            "work, DIY projects, motorcycle riding, and \u2014 if uncovered \u2014 your monocular "
            "vision), not just a generic safety pitch. If the assessment is shallow or "
            "misses most of these factors, default to your cost-conscious instinct and "
            "lean toward the cheaper option. Notice and react naturally to whether the "
            "optician documents the recommendation and your final decision."
        ),
    },
}

# Shared scoring rubric applied to all five scenarios (100 points total).
RUBRIC = [
    {"category": "Visual Needs Assessment", "points": 10},
    {"category": "Lifestyle/Risk Discovery", "points": 15},
    {"category": "Risk Identification", "points": 20},
    {"category": "Appropriate Recommendation", "points": 15},
    {"category": "Patient Education", "points": 15},
    {"category": "Impact Resistance Discussion", "points": 10},
    {"category": "Duty to Warn Fulfillment", "points": 10},
    {"category": "Informed Choice Support", "points": 5},
]

