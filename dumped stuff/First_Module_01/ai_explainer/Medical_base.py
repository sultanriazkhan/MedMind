
# Add at the very top of Medical_base.py
import re
from typing import Optional
from typing import Optional, Dict, Any
# ==============================================================================
# MEDICAL KNOWLEDGE BASE
# ==============================================================================
DEFAULT_EXPLANATION = {
    "meaning": "{test_name} result is {status}. This test requires interpretation by your healthcare provider in the context of your overall health.",
    "causes": "Multiple factors can affect this test result including diet, medications, hydration status, underlying medical conditions, and recent physical activity.",
    "effects": "The clinical effects depend on the degree of abnormality and your individual health status.",
    "solution": "Please consult your healthcare provider for proper interpretation and personalized recommendations based on your complete medical history."
}

MEDICAL_KNOWLEDGE_BASE = {

    # ==========================================================================
    # SECTION 1: HEMATOLOGY TESTS
    # ==========================================================================

    "cbc": {
        "Low": {
            "meaning": "Multiple blood cell lines are below normal, suggesting a systemic hematological disorder affecting red cells, white cells, or platelets (pancytopenia if all are low).",
            "causes": "Bone marrow failure (aplastic anemia), vitamin B12/folate deficiency, leukemia infiltrating marrow, chemotherapy/radiation, hypersplenism, autoimmune destruction, severe infections (HIV, TB).",
            "effects": "Fatigue, pallor, increased infection risk, bleeding tendency, shortness of breath, dizziness, easy bruising depending on which cell line is predominantly affected.",
            "solution": "Full clinical evaluation including bone marrow biopsy if pancytopenia is present. Treat the underlying cause (nutritional supplementation, G-CSF, platelet transfusion, immunosuppression). Refer to hematologist."
        },
        "High": {
            "meaning": "One or more blood cell lines are elevated beyond normal reference ranges, indicating polycythemia, leukocytosis, or thrombocytosis which may be reactive or primary (myeloproliferative).",
            "causes": "Polycythemia vera, chronic hypoxia (high altitude, COPD), infection/inflammation (leukocytosis), essential thrombocythemia, dehydration, stress response, medications (corticosteroids).",
            "effects": "Increased blood viscosity, thrombosis risk, headache, ruddy complexion (polycythemia), fever/signs of infection (leukocytosis), bleeding or clotting paradox (thrombocytosis).",
            "solution": "Identify which cell line is elevated. Investigate for myeloproliferative neoplasms (JAK2 mutation), treat underlying infections, ensure adequate hydration. Hematology referral for primary disorders."
        },
        "Normal": {
            "meaning": "All blood cell parameters (RBC, WBC, platelets, hemoglobin, hematocrit, indices) are within normal reference ranges, indicating a healthy hematopoietic system.",
            "causes": "N/A - This is a normal result.",
            "effects": "Adequate oxygen-carrying capacity, appropriate immune defense, normal hemostatic potential.",
            "solution": "Continue routine health screening annually. Maintain balanced nutrition including iron, B12, folate. Report unusual fatigue, bruising, or recurrent infections promptly."
        }
    },

    "hemoglobin": {
        "Low": {
            "meaning": "Reduced hemoglobin concentration (below 12 g/dL in women, 13 g/dL in men) indicates anemia — insufficient oxygen-carrying capacity of the blood.",
            "causes": "Iron deficiency (most common), vitamin B12/folate deficiency, chronic disease (renal failure, cancer, inflammatory disorders), hemolytic anemia, thalassemia, blood loss (GI bleed, menorrhagia), bone marrow suppression.",
            "effects": "Fatigue, pallor, dyspnea on exertion, palpitations, dizziness, headache, reduced exercise tolerance, cognitive impairment, koilonychia (iron deficiency), glossitis, angular stomatitis.",
            "solution": "Identify etiology: CBC indices (MCV), reticulocyte count, serum iron/ferritin, B12, folate, peripheral smear. Treat accordingly: oral/IV iron, B12 injections, folate supplementation, EPO in CKD, transfusion if severe (Hb <7 g/dL)."
        },
        "High": {
            "meaning": "Elevated hemoglobin (above 17 g/dL in men, 15 g/dL in women) indicates polycythemia, causing increased blood viscosity and thrombosis risk.",
            "causes": "Polycythemia vera (primary), chronic hypoxia (COPD, high altitude, sleep apnea), heavy smoking, dehydration (relative polycythemia), EPO-secreting tumors (renal cell carcinoma, hepatocellular carcinoma), anabolic steroid use.",
            "effects": "Headache, plethoric (ruddy) face, hypertension, dizziness, blurred vision, pruritus after hot bath, thrombosis (DVT, stroke, MI), hyperviscosity syndrome.",
            "solution": "Investigate for polycythemia vera (JAK2 mutation, bone marrow biopsy). Treat hypoxia (COPD management, CPAP for sleep apnea). Therapeutic phlebotomy for polycythemia vera. Hydration for relative polycythemia. Hydroxyurea if indicated."
        },
        "Normal": {
            "meaning": "Hemoglobin is within the normal physiological range (12–17 g/dL), reflecting adequate erythropoiesis and iron stores for optimal oxygen delivery.",
            "causes": "N/A - This is a normal result.",
            "effects": "Optimal tissue oxygenation, normal energy metabolism, good exercise tolerance.",
            "solution": "Maintain iron-rich diet (red meat, leafy greens, legumes), adequate B12 (dairy, eggs, meat), folate (fruits, vegetables). Annual CBC screening for at-risk groups (pregnant women, elderly, vegetarians)."
        }
    },

    "hematocrit": {
        "Low": {
            "meaning": "Hematocrit (HCT) below 36% in women or 41% in men indicates anemia — fewer red blood cells relative to total blood volume.",
            "causes": "Iron, B12, or folate deficiency, hemolytic anemia, chronic kidney disease, bone marrow failure, thalassemia, acute or chronic blood loss, overhydration (dilutional).",
            "effects": "Fatigue, breathlessness, pallor, tachycardia, reduced exercise capacity, compromised fetal development in pregnancy.",
            "solution": "Evaluate with full CBC, reticulocyte count, and iron studies. Treat underlying cause. Blood transfusion if HCT <21% or patient is symptomatic. Erythropoiesis-stimulating agents for CKD-related anemia."
        },
        "High": {
            "meaning": "Hematocrit above 54% in men or 47% in women indicates polycythemia, leading to increased blood viscosity and risk of thromboembolism.",
            "causes": "Dehydration, polycythemia vera, chronic hypoxic states (COPD, high altitude), testosterone/EPO abuse, smoking, sleep apnea.",
            "effects": "Increased clotting risk, headache, dizziness, ruddy complexion, hypertension, visual disturbances, possible stroke or MI.",
            "solution": "Ensure adequate hydration. Investigate for polycythemia vera with JAK2 mutation testing. Phlebotomy to maintain HCT <45%. Treat underlying hypoxic disorder. Smoking cessation."
        },
        "Normal": {
            "meaning": "Hematocrit is within normal range (36–47% women, 41–53% men), confirming appropriate red blood cell mass and plasma volume balance.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal blood viscosity, efficient oxygen transport, adequate circulatory function.",
            "solution": "Maintain hydration, balanced nutrition, routine annual blood work. Avoid high-altitude prolonged exposure without acclimatization."
        }
    },

    "rbc_count": {
        "Low": {
            "meaning": "RBC count below normal (men <4.5 million/µL, women <4.0 million/µL) reflects decreased red cell production, increased destruction, or blood loss — confirming anemia.",
            "causes": "Iron/B12/folate deficiency, aplastic anemia, hemolysis, chronic disease, bone marrow infiltration, leukemia, renal failure (reduced EPO), hemorrhage.",
            "effects": "Tissue hypoxia, fatigue, pallor, dyspnea, tachycardia, cognitive slowing, fetal growth restriction in pregnancy.",
            "solution": "Correlate with hemoglobin, MCV, MCHC for anemia classification. Treat nutritional deficiencies, manage chronic disease, consider EPO therapy, transfuse if critical."
        },
        "High": {
            "meaning": "RBC count above 5.9 million/µL (men) or 5.2 million/µL (women) indicates polycythemia — excessive red cell production or relative increase due to reduced plasma volume.",
            "causes": "Polycythemia vera, chronic hypoxia, dehydration, high altitude, EPO-producing tumors, androgen excess, smoking.",
            "effects": "Hyperviscosity, thrombosis, hypertension, headache, splenomegaly, increased risk of cardiovascular events.",
            "solution": "Identify primary vs. secondary polycythemia. Phlebotomy, hydroxyurea, or ruxolitinib for polycythemia vera. Treat hypoxic cause. Correct dehydration."
        },
        "Normal": {
            "meaning": "RBC count is within physiological range, confirming normal erythropoiesis and adequate red blood cell mass.",
            "causes": "N/A - This is a normal result.",
            "effects": "Efficient oxygen delivery to all tissues, balanced blood viscosity.",
            "solution": "Routine annual CBC. Iron-rich, balanced diet. Avoid unnecessary NSAID use that may cause GI blood loss."
        }
    },

    "wbc_count": {
        "Low": {
            "meaning": "WBC count below 4,000/µL (leukopenia) indicates reduced immune defense capacity, increasing susceptibility to infections.",
            "causes": "Viral infections (HIV, hepatitis, EBV, CMV), bone marrow suppression (chemotherapy, radiation), autoimmune conditions (SLE, rheumatoid arthritis), aplastic anemia, drug reactions (clozapine, carbimazole, methotrexate), hypersplenism.",
            "effects": "Increased frequency and severity of bacterial, viral, and fungal infections. Fever, mouth ulcers, sepsis risk. Neutropenic patients at risk for life-threatening opportunistic infections.",
            "solution": "Identify cause with differential count (which WBC type is low). Discontinue offending drugs. G-CSF (filgrastim) for chemotherapy-induced neutropenia. Prophylactic antibiotics/antifungals. Bone marrow evaluation if persistent."
        },
        "High": {
            "meaning": "WBC count above 11,000/µL (leukocytosis) indicates an immune response to infection, inflammation, or a primary bone marrow disorder.",
            "causes": "Bacterial infections, stress response, corticosteroid use, leukemia (CML, ALL, CLL), inflammatory diseases, tissue necrosis, smoking, post-splenectomy, medications (lithium, beta-agonists).",
            "effects": "Fever, fatigue, splenomegaly (in leukemia), hyperviscosity (if extreme leukocytosis >100,000/µL), increased thrombosis risk.",
            "solution": "Differential WBC count to identify predominant cell type. Peripheral smear for blasts. Treat underlying infection. Bone marrow biopsy if leukemia suspected. Urgent cytoreduction for leukostasis."
        },
        "Normal": {
            "meaning": "White blood cell count is within normal range (4,000–11,000/µL), indicating a functioning immune system without active infection or hematologic disorder.",
            "causes": "N/A - This is a normal result.",
            "effects": "Adequate immune surveillance, normal inflammatory response capacity.",
            "solution": "Maintain vaccinations, hygiene, healthy lifestyle to support immune function. Repeat CBC annually."
        }
    },

    "platelet_count": {
        "Low": {
            "meaning": "Platelet count below 150,000/µL (thrombocytopenia) impairs primary hemostasis, increasing bleeding risk at counts below 50,000/µL and spontaneous bleeding below 20,000/µL.",
            "causes": "ITP (autoimmune destruction), dengue fever, heparin-induced thrombocytopenia (HIT), DIC, bone marrow failure, liver disease (hypersplenism), viral infections (HIV, CMV), B12/folate deficiency, thrombotic thrombocytopenic purpura (TTP).",
            "effects": "Petechiae, purpura, easy bruising, mucosal bleeding (gingival, nasal), prolonged bleeding from cuts, menorrhagia, intracranial hemorrhage in severe thrombocytopenia.",
            "solution": "Treat underlying cause. Avoid antiplatelet drugs and NSAIDs. Platelet transfusion if <10,000/µL or active bleeding with <50,000/µL. IVIG or steroids for ITP. Emergency treatment for TTP with plasma exchange."
        },
        "High": {
            "meaning": "Platelet count above 450,000/µL (thrombocytosis) may be reactive or due to a primary myeloproliferative disorder (essential thrombocythemia).",
            "causes": "Reactive: iron deficiency, inflammation, infection, post-splenectomy, tissue injury. Primary: essential thrombocythemia, polycythemia vera, CML, myelofibrosis.",
            "effects": "Thrombosis risk (DVT, stroke, MI) and paradoxical bleeding in extreme thrombocytosis (>1,000,000/µL) due to acquired von Willebrand deficiency. Headache, erythromelalgia (burning pain in extremities).",
            "solution": "Determine reactive vs. primary (JAK2/CALR/MPL mutations, bone marrow biopsy). Treat iron deficiency/infection. Aspirin for thrombosis risk in essential thrombocythemia. Hydroxyurea or anagrelide for cytoreduction."
        },
        "Normal": {
            "meaning": "Platelet count is within normal physiological range (150,000–450,000/µL), ensuring effective primary hemostasis and normal clot formation.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal wound healing, appropriate clot formation, no excessive bleeding or clotting tendency.",
            "solution": "Avoid unnecessary NSAIDs/antiplatelet agents. Maintain adequate nutrition (B12, folate). Routine monitoring for patients on anticoagulants."
        }
    },

    "esr": {
        "Low": {
            "meaning": "ESR below 2 mm/hr is rare but may occur in conditions that alter red blood cell aggregation, such as polycythemia or sickle cell disease.",
            "causes": "Polycythemia vera, sickle cell disease, hyperviscosity states, severe congestive heart failure, hypofibrinogenemia.",
            "effects": "Low ESR itself causes no symptoms; it reflects underlying disease altering erythrocyte sedimentation physics.",
            "solution": "Investigate for polycythemia or sickle cell disease. Low ESR is rarely clinically significant in isolation."
        },
        "High": {
            "meaning": "Elevated ESR (above 20 mm/hr in men, 30 mm/hr in women, adjusted for age) is a non-specific marker of systemic inflammation, infection, tissue injury, or malignancy.",
            "causes": "Infections (TB, bacterial endocarditis, osteomyelitis), autoimmune diseases (rheumatoid arthritis, SLE, vasculitis), malignancy (multiple myeloma, lymphoma), giant cell arteritis, polymyalgia rheumatica, anemia, pregnancy, chronic kidney disease.",
            "effects": "Reflects but does not cause symptoms; patients have symptoms of the underlying inflammatory/infective process: fever, pain, fatigue, weight loss.",
            "solution": "ESR is a screening marker — identify the underlying cause with CRP, CBC, ANA, RF, SPEP, blood cultures, TB testing, imaging as clinically indicated. Treat the underlying condition; ESR normalizes with successful treatment."
        },
        "Normal": {
            "meaning": "ESR within normal limits indicates absence of significant systemic inflammation or acute phase response.",
            "causes": "N/A - This is a normal result.",
            "effects": "No active systemic inflammatory process detected.",
            "solution": "Normal ESR does not exclude localized disease. Continue clinical evaluation based on symptoms. Repeat if clinical suspicion of inflammatory disease persists."
        }
    },

    "pcv": {
        "Low": {
            "meaning": "PCV (Packed Cell Volume / Hematocrit) below normal indicates reduced red cell mass — anemia of varying etiology.",
            "causes": "Iron deficiency anemia, hemolytic anemia, aplastic anemia, chronic disease anemia, B12/folate deficiency, overhydration, hemorrhage.",
            "effects": "Reduced oxygen transport, fatigue, pallor, dyspnea, reduced physical performance.",
            "solution": "Full hematological evaluation (CBC indices, iron studies, reticulocyte count). Treat underlying cause with iron, B12, folate, or transfusion as appropriate."
        },
        "High": {
            "meaning": "PCV above 54% (men) or 47% (women) indicates polycythemia or dehydration, increasing blood viscosity.",
            "causes": "Dehydration, polycythemia vera, chronic hypoxia, high altitude, EPO abuse.",
            "effects": "Hyperviscosity, thrombosis, headache, hypertension.",
            "solution": "Hydration for dehydration-related elevation. Phlebotomy and hydroxyurea for polycythemia vera. Treat underlying hypoxic state."
        },
        "Normal": {
            "meaning": "PCV is within normal physiological range, reflecting an appropriate balance of red blood cells and plasma volume.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal oxygen carrying capacity and blood viscosity.",
            "solution": "Maintain hydration and balanced nutrition. Annual health screening."
        }
    },

    "mcv": {
        "Low": {
            "meaning": "MCV below 80 fL indicates microcytic anemia — red blood cells are abnormally small, most often due to impaired hemoglobin synthesis.",
            "causes": "Iron deficiency anemia (most common), thalassemia (alpha or beta), anemia of chronic disease (sometimes), sideroblastic anemia, lead poisoning.",
            "effects": "Pale, small red cells carry less oxygen. Fatigue, pallor, koilonychia (spoon nails) in iron deficiency. Splenomegaly and bony changes in thalassemia major.",
            "solution": "Measure serum ferritin, iron, TIBC to distinguish iron deficiency from thalassemia (ferritin low in IDA, normal/high in thalassemia). Hemoglobin electrophoresis for thalassemia. Iron supplementation for IDA. Genetic counseling for thalassemia."
        },
        "High": {
            "meaning": "MCV above 100 fL indicates macrocytic anemia — red blood cells are abnormally large, typically due to impaired DNA synthesis or liver disease.",
            "causes": "Vitamin B12 deficiency, folate deficiency, alcohol use disorder, hypothyroidism, liver disease, medications (methotrexate, hydroxyurea, AZT, phenytoin), myelodysplastic syndrome.",
            "effects": "Megaloblastic anemia causes fatigue, pallor; in B12 deficiency: subacute combined degeneration of spinal cord (peripheral neuropathy, ataxia, cognitive decline). Folate deficiency increases neural tube defect risk in pregnancy.",
            "solution": "Measure serum B12, folate, TSH, LFT, alcohol history, review medications. B12 injections (cyanocobalamin/hydroxocobalamin) for deficiency. Folic acid supplementation. Treat alcohol use disorder. Hematology referral for MDS."
        },
        "Normal": {
            "meaning": "MCV within 80–100 fL indicates normocytic red cells, consistent with normal red cell production.",
            "causes": "N/A - This is a normal result.",
            "effects": "Appropriately sized red cells with adequate oxygen-carrying capacity.",
            "solution": "Normocytic anemia (if anemia present) requires investigation for hemolysis, acute blood loss, chronic disease, or aplasia. No further action needed if MCV normal and other CBC indices are also normal."
        }
    },

    "mch": {
        "Low": {
            "meaning": "MCH below 27 pg indicates hypochromic red cells — less hemoglobin per cell, typically accompanying microcytic anemia.",
            "causes": "Iron deficiency anemia, thalassemia, sideroblastic anemia, lead poisoning.",
            "effects": "Pale red cells (hypochromia on smear), reduced oxygen transport, fatigue, pallor.",
            "solution": "Evaluate with serum ferritin and iron studies. Treat iron deficiency. Consider hemoglobin electrophoresis for thalassemia."
        },
        "High": {
            "meaning": "MCH above 33 pg indicates hyperchromic or macrocytic red cells with more hemoglobin per cell, typically in megaloblastic anemia or hereditary spherocytosis.",
            "causes": "B12/folate deficiency, alcohol, liver disease, hereditary spherocytosis (artifactually elevated MCH).",
            "effects": "Correlates with macrocytosis; neurological manifestations in B12 deficiency if severe.",
            "solution": "Measure B12, folate, LFT. Supplement appropriately. Osmotic fragility test and peripheral smear for spherocytosis."
        },
        "Normal": {
            "meaning": "MCH within normal range (27–33 pg) indicates normal hemoglobin content per red blood cell.",
            "causes": "N/A - This is a normal result.",
            "effects": "Red cells have appropriate hemoglobin content for effective oxygen transport.",
            "solution": "Routine health monitoring. No specific action required."
        }
    },

    "mchc": {
        "Low": {
            "meaning": "MCHC below 32 g/dL indicates hypochromic red cells with reduced hemoglobin concentration, strongly suggesting iron deficiency anemia or thalassemia.",
            "causes": "Iron deficiency anemia (most common), thalassemia, sideroblastic anemia.",
            "effects": "Reduced oxygen delivery, fatigue, pallor, characteristic hypochromic microcytic cells on peripheral smear.",
            "solution": "Evaluate iron studies. Oral ferrous sulfate for iron deficiency (150–200 mg elemental iron daily). Genetic testing for thalassemia. Dietary iron counseling."
        },
        "High": {
            "meaning": "MCHC above 36 g/dL (hyperchromia) is characteristic of hereditary spherocytosis or can occur artifactually in hemolytic states with agglutination.",
            "causes": "Hereditary spherocytosis, cold agglutinin disease (factitious), severe dehydration (rare).",
            "effects": "In hereditary spherocytosis: hemolytic jaundice, splenomegaly, gallstones, anemia of variable severity.",
            "solution": "Peripheral blood smear for spherocytes. Osmotic fragility test. Flow cytometry (EMA binding) for spherocytosis. Splenectomy in severe cases. Folic acid supplementation."
        },
        "Normal": {
            "meaning": "MCHC within 32–36 g/dL reflects normal hemoglobin concentration within red blood cells.",
            "causes": "N/A - This is a normal result.",
            "effects": "Red cells are normochromic, indicating adequate hemoglobin packing.",
            "solution": "Maintain iron-rich diet. Routine monitoring."
        }
    },

    "rdw": {
        "Low": {
            "meaning": "RDW below 11.5% is rare and not typically considered clinically significant; indicates a very uniform red blood cell population.",
            "causes": "Transfusion of uniform donor red cells, some hereditary anemias (thalassemia trait may have low-normal RDW).",
            "effects": "No direct clinical effects from low RDW.",
            "solution": "Correlate with other CBC indices. Low RDW in the setting of microcytic anemia favors thalassemia over iron deficiency."
        },
        "High": {
            "meaning": "RDW above 14.5% (anisocytosis) indicates high variability in red blood cell size, seen in nutritional deficiencies or mixed anemias before treatment response.",
            "causes": "Iron deficiency anemia, B12/folate deficiency (early), mixed deficiency anemias, hemolytic anemia, myelodysplastic syndrome, blood transfusion (donor vs. patient cells), post-treatment iron deficiency.",
            "effects": "Reflects heterogeneous red cell production; symptoms depend on the underlying anemia. High RDW + low MCV strongly suggests iron deficiency. High RDW + high MCV suggests B12/folate deficiency.",
            "solution": "Elevated RDW narrows the differential: measure iron, ferritin, B12, folate. Peripheral smear for morphology. Treat underlying nutritional deficiency. Monitor RDW normalization with treatment."
        },
        "Normal": {
            "meaning": "RDW within 11.5–14.5% indicates a uniform red blood cell population without significant size variation (no anisocytosis).",
            "causes": "N/A - This is a normal result.",
            "effects": "Uniform red cell production, consistent erythropoiesis.",
            "solution": "Normal RDW combined with low MCV favors thalassemia trait over iron deficiency. Routine monitoring as part of CBC."
        }
    },

    "peripheral_blood_smear": {
        "Low": {
            "meaning": "PBS (Peripheral Blood Smear) is a qualitative test; 'low' findings refer to decreased or absent specific cell types or morphological features suggesting bone marrow failure or severe hemolysis.",
            "causes": "Aplastic anemia (no blasts, pancytopenia), severe hemolysis, leukemia depleting normal cells.",
            "effects": "Depends on which cells are absent: anemia, infection risk, bleeding.",
            "solution": "Bone marrow aspiration/biopsy. Treat underlying hematological disorder."
        },
        "High": {
            "meaning": "Abnormal PBS findings include presence of blasts, parasites, abnormal cell morphology (sickle cells, target cells, spherocytes, schistocytes), or atypical lymphocytes, each pointing to specific disorders.",
            "causes": "Blasts (leukemia/MDS), schistocytes (microangiopathic hemolytic anemia/TTP/DIC), sickle cells (sickle cell disease), target cells (thalassemia, liver disease, iron deficiency), spherocytes (hereditary spherocytosis, autoimmune hemolysis), malaria parasites.",
            "effects": "Varies by finding: leukemia (infection/bleeding), TTP (renal failure, neurological symptoms), sickle cell (vaso-occlusive crises, stroke), malaria (fever, organ failure).",
            "solution": "PBS findings guide targeted investigation: bone marrow biopsy for blasts, direct Coombs for hemolysis, ADAMTS13 for TTP, malaria PCR/rapid test. Treat specific disorder urgently if life-threatening."
        },
        "Normal": {
            "meaning": "Peripheral blood smear shows normal cell morphology: normochromic, normocytic RBCs; normal WBC differential without blasts or dysplastic changes; normal platelet distribution.",
            "causes": "N/A - This is a normal result.",
            "effects": "Confirms healthy hematopoiesis and absence of circulating abnormal cells.",
            "solution": "No further hematological investigation required unless clinical symptoms persist. Routine health monitoring."
        }
    },

    "reticulocyte_count": {
        "Low": {
            "meaning": "Reticulocyte count below 0.5% (or absolute count <25,000/µL) indicates hypoproliferative anemia — the bone marrow is failing to produce enough red blood cells.",
            "causes": "Aplastic anemia, iron/B12/folate deficiency (before treatment), pure red cell aplasia, bone marrow infiltration (leukemia, metastatic cancer), renal failure (reduced EPO).",
            "effects": "Progressive anemia with no compensatory reticulocytosis. Fatigue, pallor, dyspnea. Absence of reticulocytosis despite anemia is a critical finding.",
            "solution": "Bone marrow evaluation essential. Erythropoietin-stimulating agents for CKD. Blood transfusion for symptomatic severe anemia. Immunosuppression/stem cell transplant for aplastic anemia. Treat nutritional deficiencies."
        },
        "High": {
            "meaning": "Elevated reticulocyte count (above 2% or >100,000/µL absolute) indicates active bone marrow erythropoietic response, most commonly due to hemolysis or acute blood loss.",
            "causes": "Hemolytic anemia (autoimmune, hereditary spherocytosis, G6PD deficiency), sickle cell crisis, acute blood loss (GI hemorrhage, trauma), recovery phase after treatment of nutritional deficiency, post-transfusion.",
            "effects": "High reticulocytes increase MCV (macrocytosis), elevate LDH and indirect bilirubin (hemolysis markers). May cause jaundice, splenomegaly in chronic hemolysis.",
            "solution": "Evaluate for hemolysis: LDH, indirect bilirubin, haptoglobin (low in hemolysis), direct Coombs test. Treat hemolytic anemia cause (steroids for autoimmune, avoid oxidant drugs in G6PD). Manage bleeding source."
        },
        "Normal": {
            "meaning": "Reticulocyte count within normal range (0.5–2.5%) confirms active but not excessive red blood cell production by the bone marrow.",
            "causes": "N/A - This is a normal result.",
            "effects": "Appropriate red cell turnover and renewal; balanced erythropoiesis.",
            "solution": "Routine monitoring. Reassuring in the context of stable hemoglobin values."
        }
    },

    "absolute_eosinophil_count": {
        "Low": {
            "meaning": "AEC below 100/µL (eosinopenia) is rarely significant clinically and is usually a stress response.",
            "causes": "Acute bacterial infections, corticosteroid excess (Cushing's syndrome, steroid therapy), acute stress, adrenocortical hyperfunction.",
            "effects": "No direct clinical manifestations. In Cushing's syndrome, eosinopenia accompanies other cortisol excess effects (hypertension, weight gain, striae).",
            "solution": "Investigate for cortisol excess if Cushing's is suspected. Otherwise, eosinopenia alone requires no treatment."
        },
        "High": {
            "meaning": "AEC above 500/µL (eosinophilia) — above 1,500/µL is hypereosinophilia — indicates allergic, parasitic, or inflammatory processes, with risk of organ damage at high levels.",
            "causes": "Allergic diseases (asthma, allergic rhinitis, atopic dermatitis), parasitic infections (Ascaris, Toxocara, Strongyloides, filariasis), drug hypersensitivity, eosinophilic esophagitis/gastroenteritis, Churg-Strauss vasculitis, hypereosinophilic syndrome, adrenal insufficiency, malignancy (Hodgkin's lymphoma).",
            "effects": "Mild eosinophilia: allergy/parasitic symptoms. Severe (>5,000/µL): eosinophilic organ infiltration causing cardiac (Löffler endocarditis), pulmonary (eosinophilic pneumonia), and neurological damage.",
            "solution": "Stool examination for parasites, IgE level, RAST testing for allergens, bone marrow biopsy if >1,500/µL. Anthelmintic therapy for parasites. Allergen avoidance. Corticosteroids for hypereosinophilic syndrome. Imatinib for FIP1L1-PDGFRA fusion positive."
        },
        "Normal": {
            "meaning": "Eosinophil count within normal range (100–500/µL) indicates appropriate immune response without active allergic or parasitic disease.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal eosinophil-mediated immune function for parasite defense and modulation of allergic inflammation.",
            "solution": "Maintain routine health practices. No specific action needed."
        }
    },

    "dlc": {
        "Low": {
            "meaning": "DLC refers to the percentage distribution of WBC types. Low individual differentials: neutropenia (<1,500/µL absolute neutrophils) indicates infection risk; lymphopenia (<1,000/µL) indicates immune suppression.",
            "causes": "Neutropenia: chemotherapy, drug-induced (clozapine, carbimazole), viral infections, aplastic anemia, SLE. Lymphopenia: HIV, TB, malnutrition, corticosteroids, radiation, SLE, immunodeficiency syndromes.",
            "effects": "Neutropenia: high risk of bacterial and fungal infections, sepsis. Lymphopenia: risk of opportunistic infections (Pneumocystis jirovecii, CMV, atypical mycobacteria).",
            "solution": "Absolute neutrophil count (ANC) <500/µL is severe — hospitalize, reverse isolation, prophylactic antibiotics, G-CSF. For lymphopenia: HIV testing, immunology workup, CD4 count. Treat underlying cause."
        },
        "High": {
            "meaning": "Elevated proportions of specific WBC types: neutrophilia (>7,500/µL) suggests bacterial infection; lymphocytosis (>4,000/µL) suggests viral infection or lymphoproliferative disorder; monocytosis, basophilia, or eosinophilia indicate specific pathological states.",
            "causes": "Neutrophilia: bacterial infections, corticosteroids, stress, CML. Lymphocytosis: viral infections (EBV, CMV, pertussis, hepatitis), CLL, ALL. Monocytosis: TB, chronic infection, monocytic leukemia. Basophilia: allergic reactions, CML.",
            "effects": "Left shift (band forms) in neutrophilia suggests severe infection. Atypical lymphocytes in EBV infection. Blast cells in leukemia.",
            "solution": "Evaluate differential in context of clinical findings. Peripheral blood smear to assess morphology. Culture and serology for infection. Bone marrow biopsy if malignancy suspected. Treat underlying disorder."
        },
        "Normal": {
            "meaning": "DLC within normal ranges: neutrophils 55–70%, lymphocytes 20–40%, monocytes 2–8%, eosinophils 1–4%, basophils 0–1%.",
            "causes": "N/A - This is a normal result.",
            "effects": "Balanced immune cell populations enabling appropriate innate and adaptive immune responses.",
            "solution": "No investigation needed. Routine annual CBC with differential for health screening."
        }
    },

    "tlc": {
        "Low": {
            "meaning": "Total Leukocyte Count below 4,000/µL (leukopenia) compromises immune defense.",
            "causes": "Viral infections, chemotherapy, aplastic anemia, SLE, hypersplenism, drug toxicity.",
            "effects": "Recurrent infections, mouth ulcers, prolonged illness, risk of sepsis.",
            "solution": "Differential count to identify which cell type is low. Bone marrow assessment if persistent. G-CSF for neutropenia. Treat underlying cause."
        },
        "High": {
            "meaning": "TLC above 11,000/µL (leukocytosis) indicates infection, inflammation, or hematological malignancy.",
            "causes": "Bacterial infections, leukemia, corticosteroid use, stress, post-splenectomy, inflammatory states.",
            "effects": "Fever, fatigue, risk of hyperviscosity at extreme counts (>100,000/µL in leukemia).",
            "solution": "Peripheral smear to identify cell type. Blood culture for infection. Bone marrow biopsy if leukemia suspected. Treat underlying cause."
        },
        "Normal": {
            "meaning": "TLC within 4,000–11,000/µL confirms an appropriate balance of immune cells.",
            "causes": "N/A - This is a normal result.",
            "effects": "Effective immune defense without pathological immune activation.",
            "solution": "Routine annual monitoring. Maintain vaccinations and healthy lifestyle."
        }
    },

    "sickling_test": {
        "Low": {
            "meaning": "Negative sickling test indicates absence of sickle hemoglobin (HbS) in blood — the red blood cells do not sickle under deoxygenating conditions.",
            "causes": "Normal hemoglobin genotype (HbAA) or absence of sickle cell gene.",
            "effects": "No risk of sickle cell disease or trait; normal red cell morphology and function.",
            "solution": "No further sickle-cell-specific testing required. Genetic counseling if family history exists."
        },
        "High": {
            "meaning": "Positive sickling test confirms presence of HbS; does not distinguish between sickle cell trait (HbAS) and sickle cell disease (HbSS). Hemoglobin electrophoresis is required for definitive diagnosis.",
            "causes": "Inheritance of one (HbAS — trait) or two (HbSS — disease) sickle cell alleles from parents of African, Middle Eastern, Indian, or Mediterranean descent.",
            "effects": "HbSS disease: vaso-occlusive pain crises, acute chest syndrome, stroke, splenic sequestration, avascular necrosis, hemolytic anemia, chronic organ damage. HbAS trait: generally asymptomatic, may have rare complications at extreme hypoxia.",
            "solution": "Confirm with hemoglobin electrophoresis (HPLC). For HbSS: hydroxyurea to increase HbF, prophylactic penicillin in children, pneumococcal vaccination, folic acid, pain management during crises, urgent blood transfusion/exchange transfusion for severe events, bone marrow transplant for severe disease."
        },
        "Normal": {
            "meaning": "Negative sickling test — no sickle hemoglobin detected.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal red blood cell morphology under deoxygenation.",
            "solution": "Genetic counseling for individuals with family history of sickle cell disease. Prenatal screening recommended for at-risk populations."
        }
    },

    "osmotic_fragility_test": {
        "Low": {
            "meaning": "Decreased osmotic fragility (red cells resist lysis in hypotonic saline) occurs when cells are flatter and more resilient, as in target cells.",
            "causes": "Iron deficiency anemia, thalassemia, liver disease, sickle cell disease (target cells are resistant to osmotic stress).",
            "effects": "Associated with underlying anemia or thalassemia symptoms.",
            "solution": "Evaluate CBC, hemoglobin electrophoresis, and iron studies to determine underlying cause."
        },
        "High": {
            "meaning": "Increased osmotic fragility means red blood cells lyse more readily in hypotonic solution, strongly suggesting hereditary spherocytosis or acquired hemolytic conditions.",
            "causes": "Hereditary spherocytosis (HS), acquired autoimmune hemolytic anemia, pyruvate kinase deficiency.",
            "effects": "Hemolytic anemia (fatigue, pallor, jaundice), splenomegaly, pigment gallstones, aplastic crises during parvovirus B19 infection.",
            "solution": "Confirm with flow cytometry (EMA binding test), direct Coombs test. Splenectomy for severe HS. Folic acid supplementation. Monitor for aplastic crises. Genetic counseling."
        },
        "Normal": {
            "meaning": "Red cells show normal osmotic fragility, indicating normal membrane structure and biconcave morphology.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal red cell membrane flexibility and survival.",
            "solution": "No further hemolysis investigation required in the absence of anemia or clinical symptoms."
        }
    },

    "g6pd_assay": {
        "Low": {
            "meaning": "G6PD enzyme activity below normal range (deficiency) indicates G6PD deficiency — an X-linked recessive disorder causing episodic hemolytic anemia upon oxidative stress.",
            "causes": "Inherited G6PD gene mutation (most common enzyme deficiency worldwide, particularly in individuals of African, Mediterranean, Middle Eastern, and South Asian descent).",
            "effects": "Episodic hemolytic anemia triggered by: oxidant drugs (primaquine, dapsone, nitrofurantoin), fava beans (favism), infections, metabolic acidosis. Symptoms: jaundice, dark urine (hemoglobinuria), fatigue, pallor. Neonatal jaundice in affected newborns.",
            "solution": "Avoid triggering agents (antimalarials, sulfonamides, nitrofurantoin, fava beans). Hydration and supportive care during hemolytic episodes. Blood transfusion for severe anemia. Folic acid supplementation. Patient and family education about triggers."
        },
        "High": {
            "meaning": "G6PD activity above normal is not clinically significant. Testing is done to detect deficiency; elevated activity has no known pathological consequence.",
            "causes": "Recent hemolytic episode reticulocytosis may elevate G6PD activity (reticulocytes have higher enzyme levels — may falsely normalize results during acute crisis).",
            "effects": "No clinical effects from elevated G6PD activity.",
            "solution": "If G6PD deficiency is clinically suspected but test is normal, repeat during non-hemolytic steady state. Molecular genetic testing if deficiency is still suspected."
        },
        "Normal": {
            "meaning": "Normal G6PD enzyme activity indicates no deficiency; red cells can withstand oxidative stress through the pentose phosphate pathway.",
            "causes": "N/A - This is a normal result.",
            "effects": "Red cells adequately protected from oxidative hemolysis.",
            "solution": "No dietary or drug restrictions required. Carrier females should be counseled about transmission risk to sons."
        }
    },

    "coombs_test": {
        "Low": {
            "meaning": "Negative Coombs test (Direct/Indirect) indicates absence of antibodies or complement bound to red blood cells, ruling out autoimmune or alloimmune hemolysis.",
            "causes": "Normal red blood cell surface without attached immunoglobulin or complement.",
            "effects": "No immune-mediated hemolysis is occurring.",
            "solution": "If hemolysis is suspected despite negative Coombs, consider non-immune causes: hereditary spherocytosis (osmotic fragility), G6PD deficiency (G6PD assay), PNH (flow cytometry), mechanical destruction."
        },
        "High": {
            "meaning": "Positive Direct Coombs Test (DAT) indicates antibodies (IgG) or complement (C3d) are attached to the patient's red blood cells — consistent with autoimmune hemolytic anemia (AIHA). Positive Indirect Coombs Test indicates alloantibodies in serum (relevant in transfusion medicine, pregnancy).",
            "causes": "Warm AIHA: IgG antibodies (idiopathic, SLE, CLL, drugs — methyldopa, penicillin). Cold AIHA: IgM antibodies (Mycoplasma pneumoniae infection, lymphoma). Transfusion reaction. Hemolytic disease of the fetus and newborn (HDFN). Drug-induced hemolytic anemia.",
            "effects": "Hemolytic anemia (variable severity): fatigue, pallor, jaundice, dark urine, splenomegaly, elevated LDH, low haptoglobin, elevated indirect bilirubin.",
            "solution": "Warm AIHA: corticosteroids (prednisolone), rituximab if refractory, splenectomy. Cold AIHA: keep patient warm, treat underlying infection/lymphoma, rituximab. Transfuse only if life-threatening (crossmatch is challenging). Folic acid supplementation."
        },
        "Normal": {
            "meaning": "Negative Coombs test confirms absence of immune-mediated red cell destruction.",
            "causes": "N/A - This is a normal result.",
            "effects": "Red cells are free from antibody/complement coating, indicating normal immune tolerance to autologous red cells.",
            "solution": "No further autoimmune hemolysis workup needed. Evaluate other causes of anemia if present."
        }
    },

    "hemoglobin_electrophoresis": {
        "Low": {
            "meaning": "Reduced proportion of normal hemoglobin variants (HbA) with compensatory increase in abnormal variants (HbS, HbC, HbF) indicates a hemoglobinopathy.",
            "causes": "Thalassemia (reduced HbA due to chain synthesis defect), sickle cell disease (HbSS replacing HbA), hemoglobin variants (HbC, HbE, HbD).",
            "effects": "Hemolytic anemia, ineffective erythropoiesis (thalassemia major), vaso-occlusion (sickle cell disease), organ damage.",
            "solution": "Molecular genetic testing for precise mutation identification. Disease-specific management: hydroxyurea, transfusion programs, iron chelation, bone marrow transplant for severe thalassemia or sickle cell disease. Genetic counseling for family planning."
        },
        "High": {
            "meaning": "Elevated HbF (>1% in adults) or HbA2 (>3.5%) provides diagnostic clues: elevated HbA2 confirms beta-thalassemia trait; elevated HbF indicates stress erythropoiesis or hereditary persistence of fetal hemoglobin (HPFH).",
            "causes": "Beta-thalassemia trait (elevated HbA2), thalassemia intermedia/major (elevated HbF), hereditary persistence of fetal hemoglobin (HPFH), sickle cell disease with high HbF (protective), response to hydroxyurea therapy.",
            "effects": "Elevated HbA2: usually asymptomatic in trait. Elevated HbF in thalassemia: mitigates disease severity. HPFH: benign condition.",
            "solution": "Genetic counseling for thalassemia trait carriers. Prenatal diagnosis for at-risk couples. Hydroxyurea to therapeutically increase HbF in sickle cell disease."
        },
        "Normal": {
            "meaning": "Hemoglobin electrophoresis pattern shows predominantly HbA (>95%), HbA2 <3.5%, HbF <1% in adults — indicating normal hemoglobin synthesis.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal hemoglobin structure with optimal oxygen affinity and red cell integrity.",
            "solution": "No further hemoglobinopathy investigation needed. Genetic counseling if family history of thalassemia or sickle cell disease."
        }
    },

    # ==========================================================================
    # SECTION 2: COAGULATION / BLEEDING PROFILE
    # ==========================================================================

    "pt": {
        "Low": {
            "meaning": "PT (Prothrombin Time) below normal reference is rare and not typically clinically significant; may indicate hypercoagulability though PT is not a sensitive marker for thrombotic risk.",
            "causes": "Pre-analytical errors, factor V Leiden mutation (does not shorten PT meaningfully), high factor VIII levels.",
            "effects": "No well-defined clinical syndrome from short PT.",
            "solution": "Repeat test to exclude laboratory error. Clinical context determines further thrombophilia workup."
        },
        "High": {
            "meaning": "Prolonged PT (above 13–16 seconds or elevated INR) indicates deficiency or dysfunction in the extrinsic/common coagulation pathway (factors VII, X, V, II, and fibrinogen), causing bleeding tendency.",
            "causes": "Warfarin therapy (intended), vitamin K deficiency (malabsorption, prolonged antibiotics, poor diet), liver disease (impaired factor synthesis), DIC, factor deficiencies, massive transfusion, rat poison ingestion (superwarfarins).",
            "effects": "Prolonged bleeding from wounds, surgical sites, GI tract. Spontaneous bruising, menorrhagia. In liver disease: variceal bleeding, coagulopathy. In DIC: simultaneous bleeding and clotting.",
            "solution": "Identify cause. For warfarin-related: hold warfarin, oral/IV vitamin K, fresh frozen plasma (FFP) or prothrombin complex concentrate (PCC) for urgent reversal. For liver disease: FFP, vitamin K, treat underlying hepatic cause. For DIC: treat trigger, FFP, cryoprecipitate, platelets."
        },
        "Normal": {
            "meaning": "PT within normal range (11–13.5 seconds) confirms intact extrinsic coagulation pathway with adequate levels of factors VII, X, V, II, and fibrinogen.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal extrinsic pathway-mediated clot formation.",
            "solution": "For patients on warfarin, PT/INR monitoring required at regular intervals as per therapeutic target. Routine preoperative check if indicated."
        }
    },

    "inr": {
        "Low": {
            "meaning": "INR below 1.0 indicates hypercoagulable state or pre-analytical error; below-therapeutic INR in anticoagulated patients means inadequate anticoagulation with continued clotting risk.",
            "causes": "Sub-therapeutic warfarin dose, warfarin resistance, drug interactions reducing warfarin effect (rifampicin, vitamin K-rich diet), laboratory error.",
            "effects": "Sub-therapeutic INR in patients with atrial fibrillation or mechanical heart valves significantly increases stroke and thromboembolic risk.",
            "solution": "Adjust warfarin dose upward. Review drug interactions and dietary vitamin K intake. Recheck INR in 1–2 weeks. Consider bridging anticoagulation if high thrombotic risk."
        },
        "High": {
            "meaning": "INR above the therapeutic range (>3.0 for most indications, or >2.5 for mechanical valves) indicates supratherapeutic anticoagulation with elevated bleeding risk.",
            "causes": "Warfarin overdose, drug interactions increasing warfarin effect (amiodarone, metronidazole, fluconazole, aspirin), liver disease, vitamin K deficiency, poor dietary intake of vitamin K.",
            "effects": "Bleeding risk: minor (bruising, nosebleeds, prolonged wound bleeding) to major (GI hemorrhage, intracranial hemorrhage). INR >5 requires urgent intervention.",
            "solution": "INR 3–5 without bleeding: reduce or hold warfarin dose. INR >5 without bleeding: oral vitamin K 1–2.5 mg. INR >5 with significant bleeding: IV vitamin K + PCC or FFP. INR >10: high risk of spontaneous intracranial hemorrhage — urgent reversal."
        },
        "Normal": {
            "meaning": "INR 0.8–1.2 in non-anticoagulated patients indicates normal coagulation. Therapeutic INR 2.0–3.0 for most anticoagulated indications represents appropriate anticoagulation.",
            "causes": "N/A - This is a normal result.",
            "effects": "Balanced hemostasis with adequate clot formation and dissolution.",
            "solution": "For patients on warfarin: monitor every 4–6 weeks once stable. Avoid NSAIDs, alcohol excess. Maintain consistent dietary vitamin K intake."
        }
    },

    "aptt": {
        "Low": {
            "meaning": "Shortened aPTT may indicate a hypercoagulable state or elevated factor VIII levels, though it is not a reliable screening test for thrombophilia.",
            "causes": "Elevated factor VIII (acute phase reactant), pregnancy, malignancy, factor V Leiden (in heterozygous state, minimally affects aPTT), pre-analytical errors (short draw, air bubbles).",
            "effects": "Clinical hypercoagulability symptoms: DVT, PE, stroke — but shortened aPTT alone is insufficient to diagnose or predict these.",
            "solution": "Repeat test to exclude pre-analytical error. Specific thrombophilia workup (factor V Leiden, protein C/S, antithrombin III) if clinically indicated."
        },
        "High": {
            "meaning": "Prolonged aPTT (above 35–40 seconds) indicates deficiency in the intrinsic/common coagulation pathway (factors VIII, IX, XI, XII, X, V, II, fibrinogen) or presence of a coagulation inhibitor.",
            "causes": "Heparin therapy (intended), hemophilia A (factor VIII deficiency), hemophilia B (factor IX deficiency), Von Willebrand disease (severe), lupus anticoagulant (antiphospholipid syndrome), DIC, liver disease, factor XII deficiency (prolonged aPTT, no bleeding), coagulation factor inhibitors.",
            "effects": "Hemophilia: deep muscle hematomas, hemarthrosis (joint bleeds), post-traumatic/surgical bleeding. Lupus anticoagulant: paradoxically increases thrombotic (not bleeding) risk. DIC: simultaneous bleeding and clotting.",
            "solution": "Mixing study (patient + normal plasma) to differentiate deficiency (corrects) from inhibitor (does not correct). Factor assays for hemophilia. Hematology referral. Factor replacement (factor VIII concentrate for hemophilia A). Manage anticoagulation for APS."
        },
        "Normal": {
            "meaning": "aPTT within normal range (25–35 seconds) confirms intact intrinsic and common coagulation pathways.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal contact activation-mediated coagulation cascade function.",
            "solution": "In heparin-anticoagulated patients, aPTT monitoring is used to titrate unfractionated heparin. Target typically 1.5–2.5x the upper limit of normal."
        }
    },

    "bleeding_time": {
        "Low": {
            "meaning": "Shortened bleeding time (below 2 minutes) is generally not clinically significant and may reflect technical variation.",
            "causes": "Technical (excessive pressure applied to testing site), laboratory variation.",
            "effects": "No clinical significance.",
            "solution": "Repeat test with standardized technique. No clinical action required."
        },
        "High": {
            "meaning": "Prolonged bleeding time (above 9 minutes) indicates defective primary hemostasis involving platelets or the vessel wall, not the coagulation cascade.",
            "causes": "Thrombocytopenia (<100,000/µL), Von Willebrand disease (VWD), platelet function disorders (Glanzmann's thrombasthenia, Bernard-Soulier syndrome), uremia (platelet dysfunction), aspirin/NSAIDs/clopidogrel use, alcohol, afibrinogenemia.",
            "effects": "Mucocutaneous bleeding: petechiae, purpura, epistaxis, gingival bleeding, menorrhagia, prolonged bleeding from superficial cuts, postoperative oozing.",
            "solution": "Check platelet count (thrombocytopenia), VWF antigen and activity, platelet aggregation studies. Treat underlying cause: DDAVP for VWD and uremia, cryoprecipitate for VWD type 3, platelet transfusion for severe thrombocytopenia, discontinue antiplatelet drugs."
        },
        "Normal": {
            "meaning": "Bleeding time within normal range (2–9 minutes) confirms adequate primary hemostasis (platelet function and vessel wall interaction).",
            "causes": "N/A - This is a normal result.",
            "effects": "Effective platelet plug formation upon vascular injury.",
            "solution": "Normal bleeding time does not exclude coagulation factor deficiencies (measured by PT/aPTT). No further platelet function testing needed without clinical indication."
        }
    },

    "clotting_time": {
        "Low": {
            "meaning": "Shortened clotting time is rarely significant and typically reflects technical variations.",
            "causes": "Pre-analytical factors, tissue thromboplastin contamination of the sample.",
            "effects": "No established clinical correlation with thrombotic risk.",
            "solution": "Repeat with proper venipuncture technique."
        },
        "High": {
            "meaning": "Prolonged clotting time indicates significant deficiency in the intrinsic coagulation pathway or presence of anticoagulants.",
            "causes": "Hemophilia A or B, severe VWD, heparin therapy, severe liver disease, DIC, coagulation factor inhibitors.",
            "effects": "Spontaneous or excessive bleeding, hemarthrosis, muscle hematomas.",
            "solution": "Correlate with aPTT and PT. Perform mixing studies and factor assays. Treat with specific factor concentrates or FFP as appropriate."
        },
        "Normal": {
            "meaning": "Clotting time within normal limits (Lee-White method: 9–12 minutes) indicates adequate intrinsic coagulation pathway function.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal clot formation through intrinsic pathway.",
            "solution": "No further coagulation investigation needed without clinical symptoms."
        }
    },

    "d_dimer": {
        "Low": {
            "meaning": "D-dimer below the cutoff (typically <500 ng/mL FEU) has a high negative predictive value for ruling out VTE (DVT, PE) in low-to-intermediate pretest probability patients.",
            "causes": "Absence of active clot formation and fibrinolysis.",
            "effects": "VTE is highly unlikely in the appropriate clinical context.",
            "solution": "If D-dimer is negative in a low pretest probability patient, VTE is effectively ruled out without imaging. No anticoagulation needed for VTE."
        },
        "High": {
            "meaning": "Elevated D-dimer indicates increased fibrin formation and degradation — a marker of active thrombosis, DIC, or other states of increased fibrinolytic activity. D-dimer is sensitive but not specific for VTE.",
            "causes": "DVT, pulmonary embolism, DIC, COVID-19 (hypercoagulability), sepsis, malignancy, recent surgery or trauma, pregnancy, advanced age, atrial fibrillation, liver disease, aortic aneurysm, postpartum state.",
            "effects": "D-dimer reflects a pathological process; clinical effects depend on the underlying condition (e.g., DVT: swollen painful leg; PE: dyspnea, pleuritic chest pain, hemoptysis; DIC: bleeding and clotting simultaneously).",
            "solution": "Use clinical prediction scores (Wells score for DVT/PE) to guide further testing. Elevated D-dimer in high pretest probability: proceed to Doppler ultrasound (DVT) or CT pulmonary angiogram (PE). For DIC: treat underlying cause, supportive coagulation replacement. Not used to monitor anticoagulation therapy."
        },
        "Normal": {
            "meaning": "D-dimer within normal range effectively rules out significant acute VTE in patients with low-to-intermediate pretest probability.",
            "causes": "N/A - This is a normal result.",
            "effects": "No evidence of active thrombus formation or significant fibrinolytic activity.",
            "solution": "In low probability clinical settings, negative D-dimer avoids unnecessary imaging. Normal D-dimer does not rule out malignancy or chronic thrombosis."
        }
    },

    "fibrinogen": {
        "Low": {
            "meaning": "Fibrinogen below 1.5 g/L (hypofibrinogenemia or afibrinogenemia) impairs clot formation and increases bleeding risk.",
            "causes": "DIC (consumptive coagulopathy), severe liver disease (reduced synthesis), L-asparaginase therapy, fibrinolytic therapy (thrombolytics), massive transfusion, congenital afibrinogenemia/hypofibrinogenemia.",
            "effects": "Failure of fibrin clot formation, mucocutaneous and surgical bleeding, delayed wound healing. In DIC: simultaneous microvascular clotting and consumption-related bleeding.",
            "solution": "Cryoprecipitate (each unit contains ~250 mg fibrinogen) to raise fibrinogen to >1.5–2 g/L. Fresh frozen plasma. Fibrinogen concentrate (RiaSTAP) if available. Treat underlying DIC cause (sepsis, obstetric complication, malignancy). Avoid fibrinolytic therapy."
        },
        "High": {
            "meaning": "Elevated fibrinogen (above 4 g/L) is an acute phase reactant indicating systemic inflammation, infection, or cardiovascular risk.",
            "causes": "Acute infection, inflammation, surgery/trauma, malignancy, cardiovascular disease, pregnancy, smoking, obesity, type 2 diabetes, nephrotic syndrome.",
            "effects": "Increased blood viscosity, elevated thrombotic risk (contributes to atherosclerosis and hypercoagulability). Elevated fibrinogen is an independent cardiovascular risk factor.",
            "solution": "Identify and treat underlying inflammatory process. Statins modestly lower fibrinogen. Lifestyle modifications (smoking cessation, weight loss, exercise). Fibrates modestly reduce fibrinogen. Elevated fibrinogen alone does not warrant anticoagulation."
        },
        "Normal": {
            "meaning": "Fibrinogen within normal range (2–4 g/L) confirms adequate clotting capacity and absence of major acute phase response.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal fibrin polymerization enabling effective clot formation.",
            "solution": "Monitor in patients at risk of DIC (sepsis, major surgery, obstetric complications). No specific action needed when normal."
        }
    },

    "fdp": {
        "Low": {
            "meaning": "FDP below detection threshold indicates no significant fibrinolytic activity, consistent with absence of major coagulopathy.",
            "causes": "Normal hemostatic state without excessive clot formation or breakdown.",
            "effects": "No excessive fibrinolysis or consumptive coagulopathy.",
            "solution": "No further coagulation investigation needed unless clinical symptoms suggest otherwise."
        },
        "High": {
            "meaning": "Elevated FDP (above 10 µg/mL) indicates excessive fibrin(ogen) degradation, seen in DIC, primary fibrinolysis, or thrombolytic therapy.",
            "causes": "DIC (most important), thrombolytic therapy (streptokinase, tPA), severe liver disease, large hematoma resorption, post-surgery, malignancy, obstetric complications (abruptio placentae, amniotic fluid embolism), PE.",
            "effects": "FDPs themselves impair platelet aggregation and fibrin polymerization, worsening the coagulopathy. Clinical bleeding, thrombosis in DIC.",
            "solution": "Diagnose DIC using DIC score (PT, aPTT, platelet, fibrinogen, D-dimer, FDP). Treat underlying trigger urgently. FFP, cryoprecipitate, platelet transfusion for supportive care. Avoid heparin unless thrombosis-predominant DIC with specialist guidance."
        },
        "Normal": {
            "meaning": "FDP within normal limits reflects minimal fibrin degradation and absence of pathological fibrinolysis.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal fibrin clot stability and homeostatic balance.",
            "solution": "No specific action. Monitor in high-risk patients (sepsis, major surgery, obstetric complications)."
        }
    },

    "thrombin_time": {
        "Low": {
            "meaning": "Shortened thrombin time is rare and not clinically significant.",
            "causes": "Pre-analytical factors, elevated fibrinogen (may paradoxically shorten TT at very high levels).",
            "effects": "No established clinical consequence.",
            "solution": "Repeat with fresh properly collected sample."
        },
        "High": {
            "meaning": "Prolonged thrombin time (above 21 seconds) indicates impaired conversion of fibrinogen to fibrin, pointing to quantitative or qualitative fibrinogen defects or the presence of anticoagulants.",
            "causes": "Heparin (even trace amounts — thrombin time is exquisitely sensitive to heparin), direct thrombin inhibitors (dabigatran, argatroban), hypofibrinogenemia or dysfibrinogenemia, high FDP (competitive inhibition), paraproteins (multiple myeloma), liver disease.",
            "effects": "Impaired final common clotting pathway; potential for bleeding if due to fibrinogen deficiency. Dabigatran toxicity risk (bleeding, stroke).",
            "solution": "Distinguish heparin effect (reptilase time is normal despite heparin), fibrinogen deficiency (measure fibrinogen level), or direct thrombin inhibitor (drug levels, ecarin clotting time). Treat fibrinogen deficiency with cryoprecipitate. Idarucizumab (Praxbind) reverses dabigatran."
        },
        "Normal": {
            "meaning": "Thrombin time within normal range confirms adequate fibrinogen quantity and function, and absence of thrombin inhibitors.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal fibrin clot formation at the final step of the coagulation cascade.",
            "solution": "Normal thrombin time with prolonged aPTT points away from fibrinogen deficiency. No specific action needed."
        }
    },

    "factor_assays": {
        "Low": {
            "meaning": "Specific coagulation factor activity below normal (typically <50% of reference) indicates factor deficiency, which may be congenital or acquired.",
            "causes": "Congenital: hemophilia A (factor VIII deficiency), hemophilia B (factor IX deficiency), hemophilia C (factor XI), VWD (VWF deficiency affecting factor VIII). Acquired: liver disease (all factors except VIII), DIC (consumptive), vitamin K deficiency (factors II, VII, IX, X), specific inhibitors (autoantibodies), massive transfusion.",
            "effects": "Mild deficiency (1–5%): severe hemophilia with spontaneous hemarthrosis and muscle bleeds. Moderate (5–30%): moderate hemophilia. Mild (30–50%): bleeding only with significant trauma/surgery. Specific factor deficiency presentation depends on pathway involved.",
            "solution": "Specific factor replacement concentrates (factor VIII for hemophilia A, factor IX for hemophilia B). Emicizumab (non-factor VIII agent for hemophilia A, especially with inhibitors). FFP for multiple factor deficiencies. Vitamin K for vitamin K-dependent factor deficiency. Hematology referral essential."
        },
        "High": {
            "meaning": "Elevated specific factor levels (e.g., factor VIII >150%) may indicate acute phase response or contribute to hypercoagulability.",
            "causes": "Elevated factor VIII: acute phase reaction (infection, inflammation, pregnancy, malignancy). Elevated factor II: genetic polymorphisms (prothrombin G20210A mutation).",
            "effects": "High factor VIII and II increase VTE risk (DVT, PE). Elevated factor V not typically associated with thrombosis.",
            "solution": "Elevated factor VIII with VTE: part of thrombophilia workup. Prothrombin G20210A mutation: consider long-term anticoagulation after first VTE especially if unprovoked. Hematology consultation."
        },
        "Normal": {
            "meaning": "All measured coagulation factor activities within normal reference range, confirming intact coagulation cascade.",
            "causes": "N/A - This is a normal result.",
            "effects": "Balanced pro- and anti-coagulant forces maintaining physiological hemostasis.",
            "solution": "No specific intervention needed. Pre-surgical screening for factor deficiencies in elective major surgery if indicated by personal/family history."
        }
    },

    # ==========================================================================
    # SECTION 3: BLOOD SUGAR / DIABETES TESTS
    # ==========================================================================

    "fasting_blood_sugar": {
        "Low": {
            "meaning": "FBS below 70 mg/dL (3.9 mmol/L) indicates hypoglycemia — insufficient glucose available for brain and body function.",
            "causes": "Insulin overdose or sulfonylurea excess (most common), prolonged fasting, alcohol ingestion (inhibits hepatic gluconeogenesis), insulinoma, Addison's disease, liver failure, reactive hypoglycemia, malnutrition.",
            "effects": "Mild: sweating, tremor, palpitations, anxiety, hunger (adrenergic symptoms). Moderate: confusion, blurred vision, weakness. Severe (<40 mg/dL): seizures, loss of consciousness, coma, permanent brain damage if prolonged.",
            "solution": "Mild-moderate: 15g fast-acting carbohydrate (glucose tablets, juice, sugar), recheck in 15 minutes. Severe/unconscious: IV dextrose (25–50 mL of 50% dextrose), glucagon injection IM/SC if IV access unavailable. Identify and treat underlying cause. Adjust insulin/sulfonylurea doses."
        },
        "High": {
            "meaning": "FBS 100–125 mg/dL indicates impaired fasting glucose (prediabetes); ≥126 mg/dL on two occasions confirms diabetes mellitus.",
            "causes": "Type 1 diabetes (autoimmune beta cell destruction), Type 2 diabetes (insulin resistance with progressive beta cell failure), gestational diabetes, MODY (maturity-onset diabetes of the young), pancreatitis/pancreatic carcinoma, Cushing's syndrome, acromegaly, medications (corticosteroids, thiazides, antipsychotics), stress hyperglycemia.",
            "effects": "Acute: polyuria, polydipsia, polyphagia, weight loss (T1DM), diabetic ketoacidosis (T1DM), hyperosmolar hyperglycemic state (T2DM). Chronic: diabetic retinopathy, nephropathy, peripheral neuropathy, autonomic neuropathy, atherosclerotic cardiovascular disease, poor wound healing.",
            "solution": "Prediabetes: lifestyle modifications (weight loss 5–7%, 150 min/week moderate exercise, dietary carbohydrate restriction), metformin if high risk. T2DM: metformin first line, add SGLT2 inhibitors, GLP-1 agonists (cardiovascular/renal benefit), DPP-4 inhibitors, insulin as needed. T1DM: intensive insulin therapy. Target FBS <130 mg/dL for most patients. Annual HbA1c monitoring."
        },
        "Normal": {
            "meaning": "FBS between 70–99 mg/dL confirms normal glucose regulation by insulin, glucagon, and hepatic glucose output.",
            "causes": "N/A - This is a normal result.",
            "effects": "Adequate brain and tissue glucose supply; normal metabolic state.",
            "solution": "Maintain healthy weight, balanced diet (low glycemic index foods, fiber), regular physical activity. Screen annually if risk factors present (obesity, family history, hypertension, dyslipidemia, history of GDM)."
        }
    },

    "random_blood_sugar": {
        "Low": {
            "meaning": "RBS below 70 mg/dL at any time indicates hypoglycemia requiring immediate assessment and intervention.",
            "causes": "Insulin overdose, sulfonylurea, prolonged fasting, alcohol, insulinoma, critical illness.",
            "effects": "Adrenergic symptoms progressing to neuroglycopenic symptoms (confusion, seizure, coma) if severe and untreated.",
            "solution": "Immediate oral glucose if conscious; IV dextrose or IM glucagon if unconscious. Identify precipitating cause."
        },
        "High": {
            "meaning": "RBS ≥200 mg/dL with symptoms (polyuria, polydipsia, unexplained weight loss) is diagnostic of diabetes mellitus regardless of fasting status.",
            "causes": "Undiagnosed or poorly controlled diabetes, stress hyperglycemia, corticosteroid use, acute illness, dietary excess, pancreatitis.",
            "effects": "Osmotic symptoms, risk of DKA (Type 1) or HHS (Type 2), chronic microvascular and macrovascular complications.",
            "solution": "Confirm with FBS or HbA1c. Initiate appropriate antidiabetic therapy. Patient education on self-monitoring, diet, and medication adherence."
        },
        "Normal": {
            "meaning": "RBS below 140 mg/dL at any random time point suggests normal glucose metabolism.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal postprandial glucose handling by pancreatic insulin secretion.",
            "solution": "Periodic fasting glucose and HbA1c screening for high-risk individuals. Maintain healthy lifestyle."
        }
    },

    "ppbs": {
        "Low": {
            "meaning": "PPBS below 70 mg/dL at 2 hours post-meal indicates postprandial hypoglycemia (reactive hypoglycemia), uncommon but clinically significant.",
            "causes": "Reactive hypoglycemia (excessive insulin response), early dumping syndrome (post-gastric surgery), insulinoma (rarely), non-islet cell tumor hypoglycemia.",
            "effects": "Sweating, tremor, hunger, palpitations, and weakness appearing 1–3 hours after meals.",
            "solution": "Low glycemic index diet, frequent small meals, avoid refined sugars. OGTT with insulin levels to characterize. Evaluate for post-surgical anatomy. Treat dumping syndrome with dietary adjustments."
        },
        "High": {
            "meaning": "PPBS ≥200 mg/dL at 2 hours post-meal (by WHO criteria) indicates diabetes mellitus; 140–199 mg/dL indicates impaired glucose tolerance (prediabetes).",
            "causes": "Diabetes mellitus type 1 or 2, inadequate antidiabetic therapy, carbohydrate-rich meal, impaired first-phase insulin secretion (early T2DM), gestational diabetes.",
            "effects": "Postprandial hyperglycemia is an independent risk factor for cardiovascular disease, retinopathy, and all-cause mortality even when FBS is normal.",
            "solution": "Dietary carbohydrate restriction, post-meal exercise (walking 15–30 minutes), alpha-glucosidase inhibitors (acarbose), short-acting insulin secretagogues, GLP-1 agonists. Adjust insulin doses in T1DM for meal carbohydrate content."
        },
        "Normal": {
            "meaning": "PPBS below 140 mg/dL at 2 hours post-meal confirms adequate post-meal insulin response and glucose disposal.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal postprandial glucose excursion with rapid glucose clearance.",
            "solution": "Low-glycemic diet, portion control. Annual diabetes screening for at-risk individuals."
        }
    },

    "hba1c": {
        "Low": {
            "meaning": "HbA1c below 4% may indicate hemolytic anemia, acute blood loss, or chronic renal failure with erythropoietin treatment (shorter RBC lifespan reduces glycation time) — or erroneously indicate tight glucose control.",
            "causes": "Hemolytic anemia (RBCs destroyed before full glycation), iron deficiency anemia recovery (new RBCs are young, less glycated), post-transfusion state, sickle cell disease, G6PD deficiency-related hemolysis, CKD on EPO therapy.",
            "effects": "Low HbA1c in the absence of true hypoglycemia reflects shortened red cell lifespan, not actual glucose control. Risk of false reassurance in diabetic management.",
            "solution": "Use alternative glycemic monitoring (fructosamine, continuous glucose monitoring) in conditions that alter red cell lifespan. Treat underlying hemolytic disorder."
        },
        "High": {
            "meaning": "HbA1c reflects average blood glucose over the preceding 2–3 months: 5.7–6.4% indicates prediabetes; ≥6.5% on two occasions confirms diabetes mellitus. Higher values indicate progressively poorer glycemic control.",
            "causes": "Poor diet adherence, medication non-compliance, inadequate antidiabetic regimen, clinical inertia, insulin resistance, stress hyperglycemia, iron deficiency (falsely elevates HbA1c), asplenia.",
            "effects": "HbA1c >7%: increased risk of retinopathy, nephropathy, neuropathy, and cardiovascular events. HbA1c >10%: very high risk; risk of DKA (T1DM) or HHS (T2DM). HbA1c >12%: symptomatic hyperglycemia, hospitalization risk.",
            "solution": "Target HbA1c <7% for most diabetic patients, <8% for elderly with multiple comorbidities. Intensify antidiabetic therapy (metformin, SGLT2 inhibitors with cardiovascular/renal benefit, GLP-1 agonists, basal insulin). Diabetes self-management education (DSME). Dietary counseling and weight management."
        },
        "Normal": {
            "meaning": "HbA1c below 5.7% indicates normal average blood glucose with no insulin resistance or diabetes.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal erythrocyte hemoglobin glycation, reflecting consistently normal blood glucose levels.",
            "solution": "Annual HbA1c screening if risk factors present (obesity, family history, hypertension, dyslipidemia). Maintain healthy lifestyle. Current WHO recommendation: screen all adults >45 years."
        }
    },

    "ogtt": {
        "Low": {
            "meaning": "Hypoglycemia during or after OGTT (below 70 mg/dL) may occur in reactive hypoglycemia — an exaggerated insulin response to glucose load.",
            "causes": "Reactive hypoglycemia, post-gastric surgery dumping syndrome, insulinoma (rare), nesidioblastosis.",
            "effects": "Symptoms at 2–4 hours post-glucose load: sweating, tremor, hunger, palpitations, confusion.",
            "solution": "Extended 5-hour OGTT with insulin levels. Dietary modification (low-GI foods, small frequent meals). Evaluate for insulinoma with 72-hour fasting test."
        },
        "High": {
            "meaning": "2-hour OGTT glucose ≥200 mg/dL: diabetes mellitus; 140–199 mg/dL: impaired glucose tolerance (IGT) — prediabetes. In pregnancy: gestational diabetes mellitus (GDM) has lower diagnostic thresholds.",
            "causes": "Insulin resistance, impaired beta cell function, hormonal excess (Cushing's, acromegaly), medications, genetic predisposition.",
            "effects": "Prediabetes/IGT: 5–10% annual progression to T2DM, cardiovascular risk. GDM: macrosomia, neonatal hypoglycemia, increased cesarean risk, maternal T2DM risk post-pregnancy.",
            "solution": "IGT: intensive lifestyle intervention (7% weight loss, 150 min exercise/week) reduces diabetes progression by 58%. Metformin for high-risk prediabetes. GDM: dietary management, insulin or metformin; deliver at 38–39 weeks for GDM on pharmacotherapy. Postpartum OGTT at 6–12 weeks."
        },
        "Normal": {
            "meaning": "Fasting glucose <100 mg/dL and 2-hour OGTT glucose <140 mg/dL confirms normal glucose tolerance and insulin sensitivity.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal incremental insulin response to glucose load with adequate glucose disposal.",
            "solution": "Normal OGTT effectively rules out diabetes and prediabetes. Repeat in 1–3 years if risk factors are present."
        }
    },

    "insulin_level": {
        "Low": {
            "meaning": "Fasting insulin below 2 µIU/mL (with high glucose) confirms absolute insulin deficiency, consistent with Type 1 diabetes or late-stage Type 2 diabetes with beta cell exhaustion.",
            "causes": "Type 1 diabetes mellitus (autoimmune beta cell destruction), late T2DM with beta cell failure, MODY subtypes, pancreatectomy, pancreatitis, chronic malnutrition.",
            "effects": "Hyperglycemia, diabetic ketoacidosis risk (particularly T1DM), weight loss, ketosis, polyuria, polydipsia.",
            "solution": "Insulin replacement therapy is mandatory in absolute deficiency. Basal-bolus insulin regimen for T1DM. Measure C-peptide and anti-GAD antibodies to differentiate T1DM from T2DM."
        },
        "High": {
            "meaning": "Elevated fasting insulin (above 25 µIU/mL) with normal or elevated glucose indicates insulin resistance — the hallmark of metabolic syndrome, prediabetes, and T2DM.",
            "causes": "Insulin resistance (obesity, metabolic syndrome, PCOS), Type 2 diabetes, insulinoma (very high insulin with low glucose), Cushing's syndrome, acromegaly, medications (corticosteroids), overeating, sedentary lifestyle.",
            "effects": "Compensatory hyperinsulinemia accelerates atherosclerosis, hypertension, dyslipidemia, and PCOS manifestations. Insulinoma: recurrent episodes of hypoglycemia.",
            "solution": "Lifestyle modification (weight loss, exercise, low-carbohydrate diet) reduces insulin resistance. Metformin, SGLT2 inhibitors. For insulinoma: 72-hour fast test, CT pancreas, surgical resection."
        },
        "Normal": {
            "meaning": "Fasting insulin within normal range (2–25 µIU/mL) with normal glucose indicates appropriate insulin secretion and sensitivity.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal beta cell function and peripheral tissue insulin sensitivity.",
            "solution": "Maintain healthy weight and active lifestyle to preserve insulin sensitivity. Insulin resistance develops gradually — routine metabolic screening in at-risk individuals."
        }
    },

    "c_peptide": {
        "Low": {
            "meaning": "C-peptide below 0.5 ng/mL in the context of hyperglycemia or hypoglycemia indicates impaired endogenous insulin secretion (absolute deficiency) or exogenous insulin administration.",
            "causes": "Type 1 diabetes mellitus (autoimmune beta cell destruction), factitious hypoglycemia from exogenous insulin injection (suppresses endogenous secretion), pancreatectomy, advanced T2DM with beta cell burnout.",
            "effects": "Absolute insulin deficiency in T1DM: DKA, weight loss, osmotic symptoms. Exogenous insulin hypoglycemia: severe hypoglycemia with suppressed C-peptide — forensic and clinical diagnostic importance.",
            "solution": "T1DM: insulin replacement mandatory. For factitious hypoglycemia: measure C-peptide and proinsulin together — exogenous insulin causes low C-peptide and proinsulin but elevated insulin levels."
        },
        "High": {
            "meaning": "Elevated C-peptide (above 3.8 ng/mL) in the context of hypoglycemia strongly suggests insulinoma; in hyperglycemia, indicates insulin resistance or non-insulin-dependent hypoglycemia.",
            "causes": "Insulinoma (neoplastic beta cell tumor — elevated C-peptide + elevated insulin + hypoglycemia is the classic triad), sulfonylurea abuse (stimulates endogenous insulin secretion), insulin resistance (T2DM, metabolic syndrome), renal failure (reduced C-peptide clearance).",
            "effects": "Insulinoma: recurrent spontaneous fasting hypoglycemia, weight gain (from eating to prevent symptoms), neuroglycopenic symptoms (seizures, cognitive impairment).",
            "solution": "72-hour supervised fast with glucose, insulin, C-peptide, proinsulin monitoring for insulinoma diagnosis. CT/MRI/endoscopic ultrasound for tumor localization. Surgical resection for insulinoma. Diazoxide or octreotide for pre-surgical medical management."
        },
        "Normal": {
            "meaning": "C-peptide within normal range (0.5–3.8 ng/mL) confirms adequate endogenous insulin production proportionate to metabolic demand.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal pancreatic beta cell secretory function.",
            "solution": "Normal C-peptide rules out insulinoma and absolute insulin deficiency in the appropriate clinical context. Routine monitoring not required."
        }
    },

    "urine_sugar": {
        "Low": {
            "meaning": "Absence of glucose in urine is the expected normal finding; detection threshold (renal threshold) is approximately 180 mg/dL blood glucose.",
            "causes": "Normal blood glucose level below renal threshold, or reduced renal tubular glucose reabsorption (renal glycosuria — rare benign condition).",
            "effects": "No clinical effects from absent urine glucose.",
            "solution": "Absence of glucosuria does not exclude diabetes if blood glucose is below the renal threshold. Confirm diabetes with blood glucose and HbA1c."
        },
        "High": {
            "meaning": "Presence of glucose in urine (glucosuria) indicates blood glucose has exceeded the renal threshold (approximately 180 mg/dL), or renal tubular glucose reabsorption is impaired.",
            "causes": "Diabetes mellitus (hyperglycemia exceeding renal threshold), renal glycosuria (normal blood glucose but defective SGLT2 renal transporter — benign condition), pregnancy (lowered renal threshold), Fanconi syndrome, acute tubular necrosis.",
            "effects": "In diabetes: glucosuria is a marker of poor glycemic control; glucose in urine predisposes to urinary tract infections. In renal glycosuria: asymptomatic but may be confused with diabetes.",
            "solution": "Confirm blood glucose and HbA1c to differentiate diabetes from renal glycosuria. SGLT2 inhibitors pharmacologically induce glucosuria as a therapeutic mechanism. Treat underlying diabetes. In pregnancy, monitor with fasting blood glucose."
        },
        "Normal": {
            "meaning": "No detectable glucose in urine, consistent with blood glucose below renal threshold and normal tubular reabsorption.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal renal glucose handling.",
            "solution": "Screen for diabetes with blood glucose testing if glucosuria is detected. Urine glucose testing is less reliable than blood glucose monitoring for diabetes management."
        }
    },

    "urine_ketones": {
        "Low": {
            "meaning": "Absence of ketones in urine is normal in non-fasting states and indicates that the body is primarily using glucose rather than fatty acid oxidation for energy.",
            "causes": "Adequate carbohydrate intake, normal insulin activity suppressing lipolysis.",
            "effects": "Normal metabolic state.",
            "solution": "No action needed. Trace ketones (1+) may be normal with prolonged fasting or a very low-carbohydrate diet."
        },
        "High": {
            "meaning": "Significant ketonuria (2+ to 4+) indicates accelerated fat catabolism and ketone body production, which may represent a medical emergency (DKA in T1DM) or a physiological response (starvation, ketogenic diet).",
            "causes": "Diabetic ketoacidosis (T1DM most commonly, T2DM rarely), starvation/prolonged fasting, alcoholic ketoacidosis, very low carbohydrate/ketogenic diet, hyperemesis gravidarum, febrile illness in children, salicylate poisoning, isopropanol ingestion.",
            "effects": "DKA: nausea, vomiting, abdominal pain, Kussmaul breathing (deep rapid respiration), acetone breath (fruity odor), dehydration, metabolic acidosis, confusion, coma if untreated. DKA mortality 1–5% despite treatment.",
            "solution": "Significant ketonuria in a diabetic patient requires immediate blood glucose, blood ketones (beta-hydroxybutyrate), arterial blood gas, electrolytes. DKA management: IV 0.9% normal saline, insulin infusion, potassium replacement, hourly monitoring, treat precipitating cause (infection, missed insulin dose). ICU admission for severe DKA."
        },
        "Normal": {
            "meaning": "No significant ketones detected in urine under normal nutritional and metabolic conditions.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal glucose-predominant energy metabolism.",
            "solution": "Monitor ketones during illness in T1DM patients (sick day rules). Educate T1DM patients to check ketones with any blood glucose >250 mg/dL."
        }
    },

    "fructosamine": {
        "Low": {
            "meaning": "Fructosamine below normal may occur in hypoalbuminemia (because it primarily reflects glycated albumin) or with genuinely low blood glucose, rather than true hypoglycemia of glycemic control significance.",
            "causes": "Hypoalbuminemia (nephrotic syndrome, liver disease, malnutrition), genuine hypoglycemia, hemolytic anemia (shortened protein turnover).",
            "effects": "Reflects underlying protein deficiency rather than glycemic control when low.",
            "solution": "Interpret fructosamine in the context of serum albumin. Correct for hypoalbuminemia or use alternative glycemic monitoring."
        },
        "High": {
            "meaning": "Elevated fructosamine (above 285 µmol/L) reflects increased glycation of serum proteins (primarily albumin), indicating poor glycemic control over the preceding 2–3 weeks.",
            "causes": "Poorly controlled diabetes mellitus (T1DM or T2DM), states where HbA1c is unreliable (hemolytic anemia, hemoglobinopathies, end-stage renal disease, pregnancy).",
            "effects": "Persistent hyperglycemia over 2–3 weeks, increased risk of diabetes complications.",
            "solution": "Intensify antidiabetic therapy. Fructosamine is particularly useful when HbA1c is unreliable (hemolytic conditions, CKD). Target fructosamine <285 µmol/L for most patients."
        },
        "Normal": {
            "meaning": "Fructosamine within 200–285 µmol/L indicates good short-term glycemic control over the preceding 2–3 weeks.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal glycation of serum albumin, reflecting well-controlled blood glucose.",
            "solution": "Continue current antidiabetic regimen. Fructosamine can complement HbA1c monitoring in specific populations."
        }
    },

    # ==========================================================================
    # SECTION 4: KIDNEY FUNCTION TESTS (KFT/RFT)
    # ==========================================================================

    "blood_urea": {
        "Low": {
            "meaning": "Blood urea below 7 mg/dL indicates reduced urea production (liver disease, low protein intake) or overhydration.",
            "causes": "Severe liver failure (impaired urea synthesis from ammonia), low-protein diet, overhydration, pregnancy (increased GFR), malnutrition.",
            "effects": "Low urea itself is not harmful; symptoms are from the underlying condition (jaundice, coagulopathy in liver failure; malnutrition effects).",
            "solution": "Investigate liver function with LFTs. Nutritional assessment. Adequate protein intake for malnourished patients."
        },
        "High": {
            "meaning": "Elevated blood urea (above 45 mg/dL) indicates increased urea production or impaired renal excretion (azotemia).",
            "causes": "Pre-renal: dehydration, heart failure, sepsis (reduced renal perfusion). Renal: acute kidney injury (AKI), chronic kidney disease (CKD), glomerulonephritis, interstitial nephritis. Post-renal: urinary obstruction (BPH, stones). Non-renal: high protein diet, GI bleed (blood protein digestion), catabolic states, corticosteroids.",
            "effects": "Uremic symptoms (when severe): nausea, vomiting, anorexia, fatigue, uremic encephalopathy (confusion, asterixis), pericarditis, pruritus.",
            "solution": "Interpret with creatinine (BUN:creatinine ratio). Pre-renal azotemia (ratio >20): aggressive fluid resuscitation. Intrinsic renal failure: identify cause, nephrology referral, dialysis if indicated. Post-renal: relieve obstruction urgently. Dietary protein restriction in advanced CKD."
        },
        "Normal": {
            "meaning": "Blood urea within normal range (7–45 mg/dL) reflects balanced protein catabolism and adequate renal urea excretion.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal nitrogen metabolism and renal handling of urea.",
            "solution": "Maintain adequate hydration and appropriate protein intake. Avoid nephrotoxic drugs (NSAIDs, aminoglycosides) without medical necessity."
        }
    },

    "serum_creatinine": {
        "Low": {
            "meaning": "Serum creatinine below 0.6 mg/dL is uncommon and may reflect reduced muscle mass rather than enhanced renal function.",
            "causes": "Reduced muscle mass (cachexia, malnutrition, elderly with sarcopenia, amputees), pregnancy (increased GFR and volume of distribution), vegetarian diet.",
            "effects": "Low creatinine may mask significant renal impairment in elderly or cachectic patients — eGFR provides better renal function estimate.",
            "solution": "Always calculate eGFR rather than relying on creatinine alone, particularly in elderly patients with low muscle mass. Nutritional support for cachexia/malnutrition."
        },
        "High": {
            "meaning": "Elevated serum creatinine (above 1.2 mg/dL in women, 1.4 mg/dL in men) indicates reduced renal filtration capacity; is a less sensitive marker (GFR must fall >50% before creatinine rises significantly).",
            "causes": "Acute kidney injury (pre-renal: dehydration, sepsis; intrinsic: ATN, glomerulonephritis, drug toxicity; post-renal: obstruction), chronic kidney disease, rhabdomyolysis (marked elevation), ingestion of cooked meat (transient), medications (trimethoprim, cimetidine — block tubular secretion without true GFR reduction).",
            "effects": "Uremic symptoms as creatinine rises (typically symptomatic >4–5 mg/dL): nausea, fatigue, fluid overload, electrolyte imbalances (hyperkalemia), metabolic acidosis, pericarditis, encephalopathy.",
            "solution": "Calculate eGFR and classify CKD stage. Identify and treat AKI cause. Avoid nephrotoxins. ACE inhibitors/ARBs for CKD with proteinuria. SGLT2 inhibitors (dapagliflozin, empagliflozin) for CKD with/without diabetes. Dialysis preparation when eGFR <15 mL/min/1.73m². Nephrology referral when creatinine >1.5 mg/dL or rapidly rising."
        },
        "Normal": {
            "meaning": "Serum creatinine within normal range (0.6–1.2 mg/dL women, 0.7–1.4 mg/dL men) indicates adequate glomerular filtration and creatinine excretion.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal muscle metabolism byproduct clearance by kidneys.",
            "solution": "Calculate eGFR for comprehensive assessment. Maintain hydration. Avoid prolonged NSAID use. Annual creatinine/eGFR monitoring for patients with hypertension, diabetes, or family history of CKD."
        }
    },

    "bun": {
        "Low": {
            "meaning": "BUN (Blood Urea Nitrogen) below 7 mg/dL indicates reduced protein catabolism or hepatic urea synthesis impairment.",
            "causes": "Liver failure, malnutrition, overhydration, very low protein diet, SIADH.",
            "effects": "Reflects underlying condition effects rather than low BUN itself.",
            "solution": "Assess liver function and nutritional status."
        },
        "High": {
            "meaning": "Elevated BUN (above 20 mg/dL) with elevated creatinine indicates azotemia. BUN/Cr ratio guides differential: >20:1 suggests pre-renal cause; <10:1 suggests intrinsic renal disease.",
            "causes": "Dehydration, heart failure, GI bleed, high protein diet, catabolic states, renal failure (pre/intrinsic/post).",
            "effects": "Uremia at high levels: fatigue, nausea, confusion, asterixis, pericarditis.",
            "solution": "Identify pre-renal, intrinsic renal, or post-renal cause using BUN/Cr ratio, urine indices, imaging. Treat accordingly."
        },
        "Normal": {
            "meaning": "BUN within 7–20 mg/dL confirms balanced nitrogen metabolism and adequate renal excretion.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal nitrogenous waste excretion.",
            "solution": "Maintain adequate hydration and protein intake appropriate for age and medical status."
        }
    },

    "uric_acid": {
        "Low": {
            "meaning": "Serum uric acid below 2.4 mg/dL (hypouricemia) is rare and may indicate xanthine oxidase deficiency or renal tubular urate wasting.",
            "causes": "Hereditary xanthinuria (xanthine oxidase deficiency), Fanconi syndrome (renal urate wasting), SIADH (dilution), allopurinol therapy, high-dose salicylates.",
            "effects": "Xanthinuria: xanthine kidney stones, myopathy (rare). Otherwise, hypouricemia itself is generally asymptomatic.",
            "solution": "Increase fluid intake to prevent xanthine stones in xanthinuria. Avoid allopurinol in xanthinuria. Identify Fanconi syndrome with urine electrolyte panel."
        },
        "High": {
            "meaning": "Elevated uric acid (above 7 mg/dL in men, 6 mg/dL in women — hyperuricemia) increases risk of gout, urate nephrolithiasis, and possibly cardiovascular disease.",
            "causes": "Gout (primary hyperuricemia), high purine diet (red meat, organ meat, shellfish, beer/alcohol), obesity, metabolic syndrome, chronic kidney disease (reduced excretion), diuretics (especially thiazides), cytotoxic therapy (tumor lysis syndrome), myeloproliferative disorders (increased cell turnover), hypothyroidism, lead poisoning (saturnine gout).",
            "effects": "Acute gout: sudden severe pain, swelling, warmth, redness (podagra — first MTP joint most common), fever. Chronic tophaceous gout: tophi deposits in ears, joints, kidney. Uric acid nephrolithiasis: renal colic. Possibly contributes to hypertension and renal disease.",
            "solution": "Acute gout: NSAIDs (indomethacin), colchicine (first-line), corticosteroids if contraindicated. Prophylaxis: allopurinol (xanthine oxidase inhibitor) or febuxostat (target uric acid <6 mg/dL). Dietary modification (low purine diet, reduce alcohol especially beer, increase low-fat dairy). Adequate hydration. Losartan (uricosuric) for hypertensive gout patients."
        },
        "Normal": {
            "meaning": "Serum uric acid within normal range (3.5–7.0 mg/dL men, 2.5–6.0 mg/dL women) indicates balanced purine metabolism and renal urate excretion.",
            "causes": "N/A - This is a normal result.",
            "effects": "No risk of gout attacks or urate crystal deposition.",
            "solution": "Maintain healthy weight, moderate alcohol consumption, adequate hydration, low-purine diet if family history of gout."
        }
    },

    "egfr": {
        "Low": {
            "meaning": "eGFR below 60 mL/min/1.73m² for >3 months defines Chronic Kidney Disease (CKD). Staging: G3a (45–59), G3b (30–44), G4 (15–29), G5 (<15, kidney failure).",
            "causes": "Diabetic nephropathy (most common in developed countries), hypertensive nephrosclerosis, glomerulonephritis, polycystic kidney disease, lupus nephritis, recurrent infections, obstructive uropathy, prolonged NSAID use, contrast nephropathy.",
            "effects": "Early CKD: often asymptomatic. Moderate-severe: hypertension, anemia (reduced EPO), hyperphosphatemia, hypocalcemia, secondary hyperparathyroidism (renal osteodystrophy), metabolic acidosis. End-stage (G5): uremic symptoms requiring dialysis or transplant.",
            "solution": "CKD management: control blood pressure (<130/80 with ACE inhibitor/ARB), control blood glucose (HbA1c <7%), restrict dietary protein (0.8 g/kg/day), SGLT2 inhibitors (reno-protective), avoid nephrotoxins, treat anemia (EPO-stimulating agents, IV iron), phosphate binders, vitamin D supplements. Nephrology referral at eGFR <30. Dialysis access planning at eGFR <20."
        },
        "High": {
            "meaning": "eGFR above normal in adults is not typically associated with pathology and may reflect normal physiological variation, hyperfiltration, or high muscle mass.",
            "causes": "Pregnancy (physiologically elevated GFR up to 50%), high dietary protein intake, early diabetic nephropathy (hyperfiltration phase — paradoxically elevated GFR with future risk of decline), high muscle mass.",
            "effects": "Hyperfiltration in early diabetes: glomerular hypertension causing future glomerulosclerosis and progressive renal damage.",
            "solution": "Monitor for microalbuminuria in diabetic patients with hyperfiltration. SGLT2 inhibitors reduce glomerular hyperfiltration and are reno-protective."
        },
        "Normal": {
            "meaning": "eGFR ≥60 mL/min/1.73m² (G1: ≥90, G2: 60–89) with no other markers of kidney damage indicates normal or mildly reduced kidney function.",
            "causes": "N/A - This is a normal result.",
            "effects": "Adequate renal filtration, excretion, and endocrine function.",
            "solution": "Annual eGFR and urine albumin:creatinine ratio monitoring for high-risk patients (diabetics, hypertensives). Maintain blood pressure <130/80 for CKD prevention."
        }
    },

    "sodium": {
        "Low": {
            "meaning": "Serum sodium below 135 mEq/L (hyponatremia) is the most common electrolyte disorder in hospitalized patients, with neurological complications when severe.",
            "causes": "SIADH (most common in hospitalized patients: medications, CNS disease, pulmonary disease, malignancy), heart failure, cirrhosis, nephrotic syndrome (hypervolemic hyponatremia), hypothyroidism, Addison's disease, diarrhea/vomiting (hypovolemic hyponatremia), beer potomania, primary polydipsia, thiazide diuretics.",
            "effects": "Mild (125–135): nausea, headache, fatigue. Moderate (120–125): confusion, gait disturbance. Severe (<120 or acute onset): cerebral edema, seizures, coma, herniation, respiratory arrest.",
            "solution": "Determine volume status (hypo/eu/hypervolemic). Isotonic saline for hypovolemic hyponatremia. Fluid restriction for SIADH and hypervolemic states. Vaptans (tolvaptan) for severe SIADH. Hypertonic saline (3%) for severe symptomatic hyponatremia — correct slowly (max 8–10 mEq/L per 24 hours) to prevent osmotic demyelination syndrome. Correct underlying cause."
        },
        "High": {
            "meaning": "Serum sodium above 145 mEq/L (hypernatremia) indicates relative water deficit or sodium excess; a serious condition with high mortality in hospitalized patients.",
            "causes": "Inadequate water intake (elderly, altered consciousness, restricted access to water), excessive water loss (diabetes insipidus — central or nephrogenic, fever, burns, diarrhea — especially secretory), excessive sodium intake (hypertonic saline, tube feeds, ingestion of seawater), hyperaldosteronism (mild).",
            "effects": "Brain cell shrinkage causing: thirst, irritability, restlessness, lethargy, seizures, coma, intracranial hemorrhage (brain vessel tearing as cells shrink).",
            "solution": "Replace free water deficit slowly (correct <10–12 mEq/L per 24 hours to prevent cerebral edema). Oral water or IV 5% dextrose water (D5W) or hypotonic saline. Treat underlying cause: DDAVP for central DI, hydrochlorothiazide/low-solute diet for nephrogenic DI."
        },
        "Normal": {
            "meaning": "Serum sodium 135–145 mEq/L reflects normal body water and sodium balance regulated by ADH and aldosterone.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal cellular hydration, neurological function, and osmotic balance.",
            "solution": "Adequate fluid intake (2–3 L/day for most adults). Limit excessive sodium intake (<2 g/day for hypertensives)."
        }
    },

    "potassium": {
        "Low": {
            "meaning": "Serum potassium below 3.5 mEq/L (hypokalemia) causes altered electrical potential of excitable cells, primarily affecting cardiac rhythm and neuromuscular function.",
            "causes": "GI losses (vomiting, diarrhea, ileostomy), renal losses (diuretics — especially loop and thiazide, hyperaldosteronism, renal tubular acidosis, amphotericin B, cisplatin), inadequate intake (anorexia, IV fluids without K+), transcellular shift into cells (alkalosis, insulin administration, beta-agonists, barium poisoning, hypokalemic periodic paralysis), magnesium deficiency (refractory hypokalemia).",
            "effects": "Muscle weakness/cramps, constipation, fatigue, polyuria (nephrogenic DI). Cardiac: PVCs, atrial fibrillation, potentially life-threatening ventricular arrhythmias (especially with digitalis use), U waves and flattened T waves on ECG.",
            "solution": "Mild (3.0–3.5): oral potassium chloride (40–80 mEq/day). Moderate-severe (<3.0 or symptomatic): IV potassium chloride (max infusion 10–20 mEq/hour via central line, continuous cardiac monitoring). Always correct hypomagnesemia simultaneously. Identify and treat underlying cause. Potassium-sparing diuretics (spironolactone, amiloride) for prevention."
        },
        "High": {
            "meaning": "Serum potassium above 5.5 mEq/L (hyperkalemia) — particularly above 6.5 mEq/L — is a life-threatening emergency due to cardiac arrhythmia risk.",
            "causes": "Reduced renal excretion (CKD, AKI, Addison's disease, type 4 RTA), medications (ACE inhibitors, ARBs, potassium-sparing diuretics, NSAIDs, trimethoprim, heparin), transcellular shift from cells (acidosis, insulin deficiency, DKA, rhabdomyolysis, tumor lysis syndrome, succinylcholine), excessive intake (IV potassium, potassium supplements, salt substitutes), pseudohyperkalemia (hemolysis of sample, prolonged tourniquet).",
            "effects": "Mild: muscle weakness, fatigue. Moderate-severe: skeletal muscle paralysis, dangerous cardiac arrhythmias: peaked T waves, widened QRS, sine wave pattern, ventricular fibrillation, asystole.",
            "solution": "ECG immediately. K+ >6.5 or with ECG changes: IV calcium gluconate (cardiac membrane stabilization — immediate). Insulin + dextrose and nebulized salbutamol (shift K+ into cells — temporary). Sodium bicarbonate if severe acidosis. Furosemide or kayexalate/patiromer (eliminate potassium). Dialysis for renal failure or refractory hyperkalemia. Hold all potassium-elevating medications."
        },
        "Normal": {
            "meaning": "Serum potassium 3.5–5.5 mEq/L ensures proper cardiac conduction, neuromuscular function, and intracellular homeostasis.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal membrane potential in cardiac and skeletal muscle, normal gastrointestinal motility.",
            "solution": "Balanced potassium intake through diet (fruits, vegetables, legumes). Monitor potassium in patients on loop diuretics or ACE inhibitors. Avoid excessive potassium supplementation without monitoring."
        }
    },

    "chloride": {
        "Low": {
            "meaning": "Serum chloride below 98 mEq/L (hypochloremia) typically occurs alongside other electrolyte and acid-base disturbances.",
            "causes": "Vomiting (loss of HCl from gastric secretions — classic cause), metabolic alkalosis, diuretic use (loop and thiazide), excessive sweating, adrenal insufficiency, SIADH (dilutional), bronchial aspiration.",
            "effects": "Usually manifests as features of metabolic alkalosis: hypoventilation, muscle cramps, weakness, tetany if alkalosis is severe.",
            "solution": "Treat underlying cause: antiemetics and fluid replacement for vomiting, sodium/potassium chloride infusion for severe deficits. Correct associated hypokalemia and alkalosis."
        },
        "High": {
            "meaning": "Serum chloride above 106 mEq/L (hyperchloremia) is commonly associated with normal anion gap metabolic acidosis.",
            "causes": "Normal anion gap metabolic acidosis: diarrhea (loss of bicarbonate), renal tubular acidosis, hyperchloremic saline infusion (0.9% NaCl excess), carbonic anhydrase inhibitors (acetazolamide), Addison's disease, urinary diversion procedures.",
            "effects": "Features of metabolic acidosis: hyperventilation (Kussmaul breathing), weakness, bone resorption with chronic acidosis, muscle wasting, growth retardation in children.",
            "solution": "Calculate anion gap and base excess. Treat underlying cause: sodium bicarbonate for severe acidosis, potassium citrate for RTA, dietary adjustments for diarrhea-related losses, appropriate IV fluid choice (Hartmann's solution preferred over normal saline to prevent hyperchloremic acidosis)."
        },
        "Normal": {
            "meaning": "Serum chloride 98–106 mEq/L reflects normal acid-base balance and electrolyte homeostasis.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal anion balance and extracellular fluid composition.",
            "solution": "Routine monitoring in patients on diuretics or with GI losses."
        }
    },

    "bicarbonate": {
        "Low": {
            "meaning": "Serum bicarbonate (HCO3) below 22 mEq/L indicates metabolic acidosis — excess acid in the body or loss of buffer.",
            "causes": "High anion gap metabolic acidosis: DKA, lactic acidosis (sepsis, ischemia), uremia, methanol/ethylene glycol/salicylate toxicity (MUDPILES mnemonic). Normal anion gap metabolic acidosis: diarrhea (HCO3 loss), renal tubular acidosis, excessive normal saline, Addison's disease.",
            "effects": "Compensatory hyperventilation (rapid deep breathing), Kussmaul respiration, weakness, lethargy, confusion, cardiac dysfunction, bone demineralization with chronic acidosis, insulin resistance.",
            "solution": "Calculate anion gap. High AG: treat underlying cause (insulin for DKA, lactate treatment, antidotes for toxic alcohol). Normal AG: sodium bicarbonate for symptomatic severe acidosis (pH <7.1), treat diarrhea, potassium citrate for RTA."
        },
        "High": {
            "meaning": "Serum bicarbonate above 26 mEq/L indicates metabolic alkalosis — excess bicarbonate or loss of acid.",
            "causes": "Vomiting (loss of HCl), nasogastric suction, loop/thiazide diuretics (volume contraction alkalosis), primary hyperaldosteronism (mineralocorticoid excess), hypokalemia, excessive antacid or bicarbonate ingestion, milk-alkali syndrome.",
            "effects": "Compensatory hypoventilation, hypocalcemia symptoms (alkalosis increases calcium binding to albumin — tetany, paresthesias, seizures), hypokalemia symptoms, confusion.",
            "solution": "Treat underlying cause: stop offending agents, correct volume depletion with isotonic saline (chloride-responsive alkalosis), correct hypokalemia (potassium chloride). Acetazolamide for chloride-resistant alkalosis. HCl infusion for severe refractory alkalosis."
        },
        "Normal": {
            "meaning": "Serum bicarbonate 22–26 mEq/L indicates normal buffering capacity and acid-base balance.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal pH maintenance and CO2 buffering.",
            "solution": "Routine monitoring in critically ill patients and those with diabetes, renal disease, or GI losses."
        }
    },

    "calcium": {
        "Low": {
            "meaning": "Serum calcium below 8.5 mg/dL (hypocalcemia) — correct for albumin (add 0.8 mg/dL for every 1 g/dL albumin below 4) — indicates reduced ionized calcium affecting neuromuscular excitability.",
            "causes": "Hypoparathyroidism (post-thyroid/parathyroid surgery most common), vitamin D deficiency, chronic kidney disease (reduced calcitriol), hypomagnesemia (impairs PTH secretion/action), pseudohypoparathyroidism, malabsorption, pancreatitis, blood transfusion (citrate chelation), hyperphosphatemia.",
            "effects": "Neuromuscular irritability: perioral paresthesias, muscle cramps, tetany, Trousseau's sign (carpal spasm with BP cuff inflation), Chvostek's sign (facial twitch with tapping facial nerve). Severe: laryngospasm, seizures, prolonged QT interval, cardiac arrhythmias.",
            "solution": "Symptomatic/severe hypocalcemia: IV calcium gluconate (1–2 g slowly over 10–20 minutes). Chronic management: oral calcium carbonate and active vitamin D (calcitriol). Treat hypomagnesemia. PTH replacement (recombinant PTH/teriparatide) for hypoparathyroidism. Vitamin D3 and calcium supplements for deficiency."
        },
        "High": {
            "meaning": "Serum calcium above 10.5 mg/dL (hypercalcemia) — symptomatic when >12 mg/dL and life-threatening when >14 mg/dL — requires urgent assessment.",
            "causes": "Primary hyperparathyroidism (most common in outpatients: usually parathyroid adenoma), malignancy (most common in hospitalized patients: PTHrP secretion, osteolytic metastases, lymphoma), vitamin D toxicity, sarcoidosis/granulomatous diseases, thiazide diuretics, lithium, milk-alkali syndrome, immobilization, Paget's disease, hyperthyroidism.",
            "effects": "Mnemonic 'Bones, Stones, Groans, Thrones, Psychic Overtones': bone pain/fractures (osteitis fibrosa cystica), renal stones (calcium oxalate/phosphate), abdominal pain/nausea/pancreatitis, polyuria/polydipsia, psychiatric symptoms (depression, confusion, psychosis). ECG: shortened QT interval.",
            "solution": "Acute severe hypercalcemia (>14 mg/dL): IV 0.9% normal saline (aggressive hydration 3–4 L over 24 hours), IV furosemide after adequate hydration, calcitonin (rapid onset but tachyphylaxis), bisphosphonates (pamidronate/zoledronate — sustained effect, takes 48–72 hours). Treat underlying cause: parathyroidectomy for hyperparathyroidism, chemotherapy for malignancy, corticosteroids for granulomatous disease/vitamin D toxicity."
        },
        "Normal": {
            "meaning": "Serum calcium 8.5–10.5 mg/dL reflects balanced PTH, vitamin D, and calcitonin regulation of calcium absorption, bone remodeling, and renal excretion.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal bone mineralization, nerve conduction, muscle contraction, and blood coagulation.",
            "solution": "Maintain adequate dietary calcium (1,000–1,200 mg/day) and vitamin D (600–800 IU/day). Sun exposure. Weight-bearing exercise for bone health."
        }
    },

    "phosphorus": {
        "Low": {
            "meaning": "Serum phosphorus below 2.5 mg/dL (hypophosphatemia) impairs cellular energy production (ATP depletion) and can cause severe multiorgan dysfunction when acute.",
            "causes": "Malnutrition/starvation, refeeding syndrome (glucose shifts phosphate into cells), hyperparathyroidism (increased renal excretion), vitamin D deficiency, chronic antacid use (phosphate binders), alcohol use disorder, Fanconi syndrome, DKA treatment (insulin drives phosphate into cells).",
            "effects": "Mild: muscle weakness, fatigue. Moderate: bone pain, rickets/osteomalacia, hemolytic anemia, platelet dysfunction. Severe (<1 mg/dL): respiratory failure (impaired diaphragm function), cardiac failure, rhabdomyolysis, encephalopathy, death.",
            "solution": "Mild (<2.5 mg/dL): oral phosphate supplements (sodium or potassium phosphate). Severe (<1 mg/dL) or symptomatic: IV sodium/potassium phosphate. Treat underlying cause. Monitor potassium during IV phosphate infusion. Prevent refeeding syndrome by introducing nutrition gradually."
        },
        "High": {
            "meaning": "Serum phosphorus above 4.5 mg/dL (hyperphosphatemia) is most commonly seen in CKD and causes calcium-phosphate precipitation, leading to vascular calcification and soft tissue calcification.",
            "causes": "Chronic kidney disease (most common — reduced renal phosphate excretion), hypoparathyroidism, pseudohypoparathyroidism, tumor lysis syndrome, rhabdomyolysis, DKA (phosphate shifts out of cells), excessive phosphate intake (phosphate-containing laxatives/enemas), vitamin D toxicity.",
            "effects": "Calcium-phosphate product >55 mg²/dL²: metastatic calcification (vascular, cardiac, soft tissue), coronary artery disease, increased mortality in CKD. Itching (pruritus), bone disease (secondary hyperparathyroidism, renal osteodystrophy). Hypocalcemia symptoms from calcium-phosphate binding.",
            "solution": "Dietary phosphate restriction (<800 mg/day). Phosphate binders with meals (calcium carbonate, sevelamer, lanthanum carbonate — non-calcium binders preferred to avoid calcium overload). Vitamin D analogs (calcitriol) and calcimimetics (cinacalcet) for secondary hyperparathyroidism. Dialysis adequacy in ESRD. Treat underlying cause."
        },
        "Normal": {
            "meaning": "Serum phosphorus 2.5–4.5 mg/dL reflects PTH- and FGF-23-mediated renal phosphate excretion and adequate dietary intake.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal energy metabolism (ATP, creatine phosphate), bone mineralization (hydroxyapatite), and cell membrane integrity.",
            "solution": "Balanced phosphate intake. Monitor phosphorus in CKD patients regularly. Avoid excessive phosphate-containing food additives."
        }
    },

    "magnesium": {
        "Low": {
            "meaning": "Serum magnesium below 1.7 mg/dL (hypomagnesemia) is common in hospitalized patients and causes refractory hypokalemia and hypocalcemia.",
            "causes": "GI losses (prolonged diarrhea, malabsorption, nasogastric suction, alcoholism), renal losses (loop diuretics, aminoglycosides, cisplatin, amphotericin B, proton pump inhibitors — chronic use, genetic tubular disorders), poor intake (malnutrition, alcoholism, post-bariatric surgery), redistribution (DKA treatment, refeeding syndrome).",
            "effects": "Neuromuscular: tremor, weakness, cramps, tetany. Cardiac: atrial fibrillation, ventricular arrhythmias (torsades de pointes especially with prolonged QT), premature beats, digoxin toxicity potentiation. Neurological: confusion, seizures. Refractory hypokalemia and hypocalcemia (magnesium required for PTH secretion and potassium channel function).",
            "solution": "Symptomatic/severe hypomagnesemia: IV magnesium sulfate (2–4 g over 15–60 minutes, then infusion). Mild: oral magnesium oxide, citrate, or glycinate. Always correct magnesium before treating refractory hypokalemia/hypocalcemia. Identify and treat underlying cause. Reduce/stop diuretics if possible. PPI deprescribing if appropriate."
        },
        "High": {
            "meaning": "Serum magnesium above 2.6 mg/dL (hypermagnesemia) is rare in patients with normal renal function; occurs mainly with excessive magnesium administration.",
            "causes": "Excessive magnesium intake (antacids, laxatives, Epsom salt, magnesium-containing enemas, IV magnesium for eclampsia), renal failure (impaired excretion), hypothyroidism, Addison's disease.",
            "effects": "Progressive toxicity: nausea/vomiting (>4 mg/dL), lethargy, areflexia (>6 mg/dL), respiratory depression (>8 mg/dL), cardiac arrest (>15 mg/dL). Loss of deep tendon reflexes is an early clinical sign of toxicity.",
            "solution": "Stop all magnesium-containing preparations. Calcium gluconate IV (10 mL of 10% solution) — antagonizes magnesium toxicity at the membrane level. IV fluids and furosemide to enhance renal excretion. Dialysis for severe hypermagnesemia with renal failure. Monitor DTRs clinically during IV magnesium therapy."
        },
        "Normal": {
            "meaning": "Serum magnesium 1.7–2.6 mg/dL supports enzyme function (300+ enzymatic reactions), neuromuscular signaling, DNA synthesis, and cardiac rhythm.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal cardiac conduction, neuromuscular function, energy metabolism, and bone mineralization.",
            "solution": "Adequate magnesium intake through diet (nuts, seeds, leafy greens, dark chocolate, whole grains). Magnesium supplementation beneficial for migraine prophylaxis, pre-eclampsia prevention, and possibly type 2 diabetes prevention."
        }
    },

    "urine_protein": {
        "Low": {
            "meaning": "Absence or trace amounts of urine protein is normal; the healthy glomerulus filters very little protein and tubular cells reabsorb most of what is filtered.",
            "causes": "Normal glomerular and tubular function.",
            "effects": "Normal kidney protein conservation.",
            "solution": "No action needed. Transient proteinuria from fever, exercise, orthostatic proteinuria in young adults is benign."
        },
        "High": {
            "meaning": "Urine protein above 150 mg/day (proteinuria) indicates glomerular or tubular damage, or overflow proteinuria from excessive plasma proteins.",
            "causes": "Glomerular: diabetic nephropathy (most common — microalbuminuria progressing to macroproteinuria), hypertensive nephrosclerosis, glomerulonephritis (IgA nephropathy, FSGS, membranous nephropathy), lupus nephritis. Tubular: interstitial nephritis, Fanconi syndrome, aminoglycoside toxicity. Overflow: multiple myeloma (Bence Jones protein), myoglobinuria, hemoglobinuria.",
            "effects": "Nephrotic range proteinuria (>3.5 g/day): hypoalbuminemia, edema, hyperlipidemia, lipiduria, hypercoagulability (loss of antithrombin III). Non-nephrotic proteinuria: progressive renal function decline over years.",
            "solution": "Quantify with spot urine albumin:creatinine ratio (ACR) or 24-hour urine collection. ACE inhibitors/ARBs reduce proteinuria and slow CKD progression (target <300 mg/day). SGLT2 inhibitors (canagliflozin, dapagliflozin) significantly reduce proteinuria. Treat underlying glomerulonephritis (immunosuppression for lupus, FSGS). Nephrotic syndrome: albumin infusion, diuretics, anticoagulation."
        },
        "Normal": {
            "meaning": "Urine protein below 150 mg/day (or ACR <30 mg/g) confirms normal glomerular filtration barrier and tubular reabsorption.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal renal protein handling and glomerular integrity.",
            "solution": "Annual urine protein screening for diabetics and hypertensives. Maintain blood pressure and glucose control to prevent proteinuria development."
        }
    },

    "microalbuminuria": {
        "Low": {
            "meaning": "Urine albumin:creatinine ratio below 30 mg/g or albumin excretion <30 mg/day indicates normal glomerular permeability to albumin.",
            "causes": "Normal glomerular basement membrane integrity without significant hypertension or diabetes-related damage.",
            "effects": "No evidence of early glomerular injury.",
            "solution": "Annual screening for diabetics and hypertensives. Continue preventive measures (blood pressure control, blood glucose control, smoking cessation)."
        },
        "High": {
            "meaning": "Microalbuminuria (30–300 mg/day or ACR 30–300 mg/g) represents early marker of glomerular endothelial dysfunction and predicts progressive diabetic nephropathy and cardiovascular risk.",
            "causes": "Diabetes mellitus (earliest measurable sign of diabetic nephropathy), hypertension, obesity, metabolic syndrome, early glomerulonephritis, smoking, acute febrile illness (transient).",
            "effects": "Diabetic nephropathy progression: micro→macro albuminuria → declining eGFR → ESRD within 10–20 years without intervention. Independent cardiovascular risk factor (endothelial dysfunction marker).",
            "solution": "ACE inhibitors or ARBs (reno-protective — target ACR <30 mg/g). SGLT2 inhibitors (empagliflozin, dapagliflozin) — superior renal protection demonstrated in major trials. Tight blood pressure control (<130/80 mmHg). Optimal glycemic control (HbA1c <7%). Smoking cessation. Finerenone (non-steroidal MRA) for additional reduction in CKD with T2DM."
        },
        "Normal": {
            "meaning": "Urine microalbumin within normal limits indicates intact glomerular filtration barrier without early diabetic or hypertensive kidney injury.",
            "causes": "N/A - This is a normal result.",
            "effects": "Preserved glomerular integrity.",
            "solution": "Annual microalbumin screening in all diabetics and hypertensives. Control blood pressure and glucose aggressively to prevent microalbuminuria from developing."
        }
    },

    # ==========================================================================
    # SECTION 5: LIVER FUNCTION TESTS (LFT)
    # ==========================================================================

    "total_bilirubin": {
        "Low": {
            "meaning": "Total bilirubin below 0.3 mg/dL has no known clinical significance.",
            "causes": "Healthy state, certain medications, or laboratory variation.",
            "effects": "No clinical effects from low bilirubin.",
            "solution": "No action required. Normal variation."
        },
        "High": {
            "meaning": "Total bilirubin above 1.2 mg/dL (hyperbilirubinemia); jaundice (icterus) becomes clinically visible when >2.5 mg/dL. Must determine if predominantly direct (conjugated) or indirect (unconjugated) to identify etiology.",
            "causes": "Prehepatic (unconjugated hyperbilirubinemia): hemolytic anemia, ineffective erythropoiesis, blood transfusion reactions, hematoma resorption, Gilbert's syndrome, Crigler-Najjar syndrome. Hepatic (mixed): hepatocellular disease (viral hepatitis, alcoholic hepatitis, NASH, drug-induced liver injury, autoimmune hepatitis, Wilson's disease). Posthepatic (conjugated): biliary obstruction (choledocholithiasis, cholangiocarcinoma, pancreatic head cancer, primary sclerosing cholangitis, primary biliary cholangitis).",
            "effects": "Jaundice (skin, sclerae), dark urine (conjugated), pale stools (obstructive), pruritus (bile salt accumulation), malabsorption of fat-soluble vitamins (obstructive). Neonatal hyperbilirubinemia: kernicterus risk (brain damage) when severely elevated in neonates.",
            "solution": "Fractionate bilirubin (direct vs indirect). Indirect dominant: hemolysis workup (LDH, haptoglobin, reticulocyte count, Coombs). Mixed/direct: ultrasound abdomen, viral hepatitis serology, liver enzymes, autoimmune markers. Obstructive: MRCP/ERCP for biliary stone removal, surgical or endoscopic decompression. Neonatal: phototherapy, exchange transfusion."
        },
        "Normal": {
            "meaning": "Total bilirubin 0.3–1.2 mg/dL indicates normal heme catabolism, hepatic conjugation, and biliary excretion.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal bilirubin metabolism and bile flow.",
            "solution": "Routine health monitoring. Avoid hepatotoxic substances (excessive alcohol, unregulated herbal supplements). Annual LFT for at-risk individuals."
        }
    },

    "alt_sgpt": {
        "Low": {
            "meaning": "ALT below normal (below 7 U/L) has no clinical significance.",
            "causes": "Normal variation, very low muscle mass, uremia (impairs enzymatic activity in some lab methods).",
            "effects": "No clinical significance.",
            "solution": "No action required."
        },
        "High": {
            "meaning": "Elevated ALT (SGPT) is a liver-specific enzyme marker; elevation indicates hepatocellular injury. ALT >3x ULN is significant. ALT/AST ratio helps characterize the cause of liver disease.",
            "causes": "Viral hepatitis (hepatitis A, B, C, D, E — markedly elevated, often >500 U/L in acute viral hepatitis), alcoholic hepatitis (typically AST:ALT ratio >2:1), NAFLD/NASH (2–5x ULN), drug-induced liver injury (NSAIDs, statins, isoniazid, paracetamol — potentially massive elevation >1000 U/L in acetaminophen toxicity), autoimmune hepatitis, ischemic hepatitis ('shock liver'), Wilson's disease, celiac disease.",
            "effects": "Right upper quadrant discomfort, fatigue, jaundice if severe, anorexia, nausea. In fulminant hepatic failure: coagulopathy, encephalopathy, renal failure.",
            "solution": "Identify etiology: hepatitis serology (HBsAg, anti-HCV, HAV IgM), autoimmune markers (ANA, ASMA, anti-LKM1), ceruloplasmin (Wilson's), alcohol history, medication review, ultrasound. Stop hepatotoxic drugs. Antiviral therapy for chronic hepatitis B (tenofovir, entecavir) and C (direct-acting antivirals). N-acetylcysteine for acetaminophen toxicity. Liver transplant referral for fulminant failure."
        },
        "Normal": {
            "meaning": "ALT within normal range (7–56 U/L) suggests intact hepatocyte integrity without significant ongoing liver cell damage.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal hepatocellular metabolic function.",
            "solution": "Avoid alcohol excess, maintain healthy weight (NAFLD prevention), take medications only as prescribed. Annual LFT screening for patients on long-term hepatotoxic medications."
        }
    },

    "ast_sgot": {
        "Low": {
            "meaning": "AST below normal has no clinical significance.",
            "causes": "Normal variation. Uremia may suppress AST activity.",
            "effects": "No clinical significance.",
            "solution": "No action required."
        },
        "High": {
            "meaning": "Elevated AST indicates hepatocellular damage or muscle injury (AST is less liver-specific than ALT, also found in cardiac muscle, skeletal muscle, kidneys, brain). AST:ALT ratio >2:1 strongly suggests alcoholic liver disease.",
            "causes": "Liver: hepatitis (viral, alcoholic, NASH, drug-induced), cirrhosis, liver cancer. Non-liver: acute MI (historically used, now superseded by troponin), rhabdomyolysis, myositis, hemolysis, strenuous exercise, cardiac surgery, hypothyroidism.",
            "effects": "Liver disease: fatigue, jaundice, abdominal pain. In MI (when primarily elevated): chest pain, cardiac dysfunction.",
            "solution": "Evaluate AST in context of ALT, LDH, troponin, CK to determine if liver or non-liver source. For liver disease: same as ALT management. For cardiac source: ECG and troponin. For muscle source: CK, myoglobin, hydration for rhabdomyolysis."
        },
        "Normal": {
            "meaning": "AST within normal range (10–40 U/L) indicates intact liver and muscle cell integrity.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal hepatocellular and muscle cell membrane integrity.",
            "solution": "Annual monitoring in patients on statins, antituberculosis therapy, or with chronic liver disease."
        }
    },

    "alp": {
        "Low": {
            "meaning": "ALP below normal (below 44 U/L) is rare and may occur in hypothyroidism, pernicious anemia, zinc deficiency, or rarely cardiopulmonary bypass.",
            "causes": "Hypothyroidism, pernicious anemia, zinc deficiency, hypophosphatemia (genetic hypophosphatasia — rare enzyme deficiency causing defective bone mineralization).",
            "effects": "Hypophosphatasia: dental abnormalities, rickets/osteomalacia, skeletal pain, fractures.",
            "solution": "Check TSH, B12, zinc levels. Genetic testing for hypophosphatasia. Asfotase alfa (enzyme replacement) for hypophosphatasia in children."
        },
        "High": {
            "meaning": "Elevated ALP has two major sources: liver (biliary tract) and bone. Elevation indicates biliary obstruction (cholestasis), liver infiltration, or high bone turnover.",
            "causes": "Liver/biliary: cholestasis (intra- or extrahepatic obstruction), primary biliary cholangitis, primary sclerosing cholangitis, biliary obstruction (stone, cancer), hepatic metastases, hepatic granulomas (sarcoidosis, TB), drug-induced cholestasis. Bone: Paget's disease, healing fractures, bone metastases, hyperparathyroidism, osteomalacia. Physiological: pregnancy (third trimester — placental ALP), childhood growth, post-meal (intestinal ALP).",
            "effects": "Cholestatic jaundice, pruritus, malabsorption if prolonged obstruction. Bone disease: bone pain, fractures (Paget's disease, osteomalacia, metastases).",
            "solution": "Fractionate ALP (GGT elevated in liver disease, not in bone disease). Ultrasound/MRCP for biliary obstruction. Bone scan/X-ray/bone-specific ALP for bone disease. Biliary decompression (ERCP, surgery) for obstruction. Bisphosphonates for Paget's disease. Treat malignancy if metastatic."
        },
        "Normal": {
            "meaning": "ALP within normal range (44–147 U/L) indicates normal bile flow, hepatic function, and bone metabolism.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal biliary excretory function and bone remodeling.",
            "solution": "Monitor ALP in patients with bone disorders or liver disease. Physiologically elevated in children and pregnancy — no action needed."
        }
    },

    "ggt": {
        "Low": {
            "meaning": "GGT below normal has no known clinical significance.",
            "causes": "Normal variation or laboratory-specific reference differences.",
            "effects": "No clinical effects.",
            "solution": "No action required."
        },
        "High": {
            "meaning": "Elevated GGT (above 60 U/L) is a sensitive but non-specific marker of hepatic and biliary disease; highly sensitive for alcohol-induced liver damage. GGT elevation with elevated ALP confirms hepatic (not bone) origin of ALP elevation.",
            "causes": "Chronic alcohol use (most sensitive marker — induced by alcohol even without liver damage), non-alcoholic fatty liver disease, biliary obstruction, cholangitis, drug-induced liver injury (anticonvulsants, barbiturates, rifampicin — enzyme inducers), viral hepatitis, hepatic metastases, hepatocellular carcinoma, pancreatic disease, heart failure (congestive hepatopathy), hyperthyroidism.",
            "effects": "Often asymptomatic when mildly elevated. Elevated GGT is an independent cardiovascular risk factor. In significant hepatic or biliary disease: fatigue, right upper quadrant discomfort, jaundice.",
            "solution": "Alcohol abstinence (GGT normalizes within 2–6 weeks of complete abstinence — useful as compliance marker). Evaluate for underlying liver disease if persistently elevated without alcohol use. Review hepatotoxic medications. Ultrasound abdomen. Lifestyle modification for NAFLD."
        },
        "Normal": {
            "meaning": "GGT within normal range (up to 60 U/L) indicates normal hepatic microsomal activity and biliary function.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal glutathione recycling and biliary transport function.",
            "solution": "GGT is the most sensitive indicator of excessive alcohol consumption. Periodic monitoring in alcoholic patients and those on liver enzyme-inducing medications."
        }
    },

    "total_protein": {
        "Low": {
            "meaning": "Total serum protein below 6.4 g/dL (hypoproteinemia) indicates reduced synthesis, increased loss, or dilution.",
            "causes": "Reduced synthesis: liver failure, severe malnutrition, malabsorption. Increased loss: nephrotic syndrome (massive proteinuria), protein-losing enteropathy, burns, exudative wounds. Increased catabolism: chronic infection, malignancy, hyperthyroidism. Dilution: overhydration, pregnancy.",
            "effects": "Hypoalbuminemia-related edema, ascites, pleural effusion (reduced oncotic pressure). Impaired drug binding (many drugs bind to albumin). Malnutrition-related immune dysfunction.",
            "solution": "Evaluate albumin, globulin separately. LFTs and nutritional assessment for reduced synthesis. 24-hour urine protein for nephrotic syndrome. Treat underlying cause. Nutritional support (high-protein diet, enteral/parenteral nutrition). Albumin infusion for symptomatic severe hypoalbuminemia."
        },
        "High": {
            "meaning": "Total protein above 8.3 g/dL (hyperproteinemia) is most commonly due to elevated globulins (paraproteinemia) or dehydration.",
            "causes": "Paraproteinemia (multiple myeloma, Waldenström's macroglobulinemia, MGUS — excess immunoglobulins), chronic infections/inflammation (elevated globulins), dehydration (relative hyperproteinemia), sarcoidosis.",
            "effects": "In multiple myeloma: bone pain, renal failure, anemia, hyperviscosity (with high IgM in Waldenström's). High globulins: elevated ESR, rouleaux formation on PBS.",
            "solution": "Serum protein electrophoresis (SPEP) to identify paraprotein band. Immunofixation electrophoresis for paraprotein characterization. Bone marrow biopsy for myeloma diagnosis. Correct dehydration. Chemotherapy/novel agents for myeloma."
        },
        "Normal": {
            "meaning": "Total protein 6.4–8.3 g/dL confirms adequate synthetic function and protein homeostasis.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal oncotic pressure, adequate drug-binding proteins, functional immune proteins.",
            "solution": "Balanced protein intake (0.8–1.2 g/kg/day for healthy adults, higher for athletes and elderly). Annual LFT monitoring for at-risk individuals."
        }
    },

    "albumin": {
        "Low": {
            "meaning": "Serum albumin below 3.5 g/dL (hypoalbuminemia) is a marker of malnutrition, liver disease, or protein loss and is associated with increased morbidity and mortality.",
            "causes": "Liver disease (reduced synthesis — cirrhosis, hepatitis), malnutrition/starvation, protein-losing enteropathy, nephrotic syndrome, burns, critical illness (negative acute phase reactant, diluted by IV fluids), malabsorption syndromes (Crohn's disease, celiac disease), hypothyroidism.",
            "effects": "Peripheral edema, ascites, pleural effusion, pulmonary edema (reduced oncotic pressure). Impaired drug binding (increases free drug fraction — toxicity risk). Wound healing impairment. Poor surgical outcomes. Hypoalbuminemia must be considered when interpreting calcium levels.",
            "solution": "High-protein diet (1.2–1.5 g/kg/day). Treat underlying condition. IV albumin infusion for spontaneous bacterial peritonitis in cirrhosis (proven mortality benefit), large volume paracentesis (>5 L), or hepatorenal syndrome type 1 (with terlipressin). Enteral nutrition in hospitalized malnourished patients."
        },
        "High": {
            "meaning": "Serum albumin above 5.0 g/dL (hyperalbuminemia) almost always reflects dehydration rather than overproduction.",
            "causes": "Dehydration (hemoconcentration), excessive IV albumin infusion, rare congenital analbuminemia (paradoxically mild hypoalbuminemia — body compensates). True hyperproteinemia is not an established clinical entity.",
            "effects": "Consequences of underlying dehydration: thirst, concentrated urine, dizziness, tachycardia.",
            "solution": "Rehydrate with oral or IV fluids. Albumin-corrected calcium must be recalculated."
        },
        "Normal": {
            "meaning": "Albumin 3.5–5.0 g/dL confirms adequate hepatic synthesis, normal capillary oncotic pressure, and good nutritional status.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal fluid distribution, drug transport, and nutritional reserve.",
            "solution": "Adequate dietary protein. Annual albumin monitoring in elderly, chronic liver disease, and CKD patients."
        }
    },

    "ag_ratio": {
        "Low": {
            "meaning": "A/G ratio below 1.0 indicates either low albumin or elevated globulins (or both), suggesting liver disease, protein-losing conditions, or paraproteinemia.",
            "causes": "Low albumin: liver disease, nephrotic syndrome, malnutrition. High globulins: chronic infections (TB, HIV, kala-azar), autoimmune diseases (SLE, rheumatoid arthritis), chronic liver disease (reactive hypergammaglobulinemia), multiple myeloma, sarcoidosis.",
            "effects": "Elevated ESR, hyperviscosity (myeloma), immune dysfunction.",
            "solution": "SPEP to characterize globulin pattern. LFTs and hepatitis serology. Autoimmune panel. Bone marrow evaluation if paraprotein detected."
        },
        "High": {
            "meaning": "A/G ratio above 2.0 may indicate low globulins (hypogammaglobulinemia) or high albumin (dehydration) — less commonly evaluated in isolation.",
            "causes": "Primary immunodeficiency (common variable immunodeficiency, X-linked agammaglobulinemia), nephrotic syndrome (selective IgG loss), immunosuppressive therapy.",
            "effects": "Hypogammaglobulinemia: recurrent bacterial infections, bronchiectasis.",
            "solution": "Quantitative immunoglobulins (IgG, IgA, IgM). Immunology referral for primary immunodeficiency. IVIG replacement for significant hypogammaglobulinemia."
        },
        "Normal": {
            "meaning": "A/G ratio between 1.0–2.0 indicates balanced albumin synthesis and globulin production.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal distribution of transport proteins and immunoglobulins.",
            "solution": "Routine monitoring as part of comprehensive metabolic panel."
        }
    },

    "serum_ammonia": {
        "Low": {
            "meaning": "Ammonia below normal has no known clinical significance.",
            "causes": "Normal nitrogen metabolism, vegetarian diet (reduced protein), laboratory variation.",
            "effects": "No clinical effects.",
            "solution": "No action required."
        },
        "High": {
            "meaning": "Serum ammonia above 50 µmol/L indicates impaired hepatic ammonia clearance (liver failure, portosystemic shunting) or increased nitrogen production, causing hepatic encephalopathy.",
            "causes": "Liver failure (acute or chronic — cirrhosis with portosystemic shunting), GI bleed (blood protein source), constipation (increased gut ammonia production), infection (GI flora ammonia production), urease-producing bacterial infection, urea cycle enzyme deficiencies (children), high-protein diet in cirrhosis, urinary tract infection with urease-producing bacteria.",
            "effects": "Hepatic encephalopathy: asterixis (flapping tremor), confusion, personality changes, disorientation, stupor, coma (grades I–IV). Cerebral edema in acute liver failure. In children with urea cycle defects: episodic vomiting, encephalopathy precipitated by protein intake.",
            "solution": "Lactulose (1st line — reduces colonic pH and traps ammonia, also acts as osmotic laxative — target 2–4 soft stools/day). Rifaximin (poorly absorbed antibiotic — reduces ammonia-producing gut bacteria). Protein restriction (temporary, not prolonged — adequate protein needed for liver recovery). Treat precipitating factors (infection, GI bleed, constipation). BCAA supplementation. Liver transplant for end-stage liver disease."
        },
        "Normal": {
            "meaning": "Serum ammonia <50 µmol/L indicates effective hepatic ammonia clearance through the urea cycle.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal hepatic detoxification and neurocognitive function.",
            "solution": "Moderate protein intake. Avoid precipitating factors for hyperammonemia in patients with liver disease."
        }
    },

    # ==========================================================================
    # SECTION 6: LIPID PROFILE
    # ==========================================================================

    "total_cholesterol": {
        "Low": {
            "meaning": "Total cholesterol below 150 mg/dL (hypocholesterolemia) may indicate malnutrition, malabsorption, or a rare inherited disorder, and is associated with increased mortality in some populations.",
            "causes": "Malnutrition, malabsorption syndromes (celiac, Crohn's), hyperthyroidism (increased catabolism), liver failure, abetalipoproteinemia (rare genetic disorder — very low or absent LDL), mandelbaum-Tanaka disease, statins (therapeutic lowering), inflammation/sepsis (negative acute phase reactant — cholesterol consumed in inflammatory response).",
            "effects": "Very low cholesterol (<100 mg/dL): potential risk of hemorrhagic stroke, depression, cancer risk (cause vs. effect debated). Fat-soluble vitamin deficiency (A, D, E, K) in severe cases. Abetalipoproteinemia: fat malabsorption, steatorrhea, retinitis pigmentosa, spinocerebellar ataxia.",
            "solution": "Investigate underlying cause (thyroid function, nutritional assessment, liver function, genetic evaluation for abetalipoproteinemia). Nutritional support. High-dose fat-soluble vitamins for abetalipoproteinemia. If due to statins: therapeutic low cholesterol is the treatment goal."
        },
        "High": {
            "meaning": "Total cholesterol above 200 mg/dL (borderline: 200–239, high: ≥240 mg/dL) is a major modifiable cardiovascular risk factor.",
            "causes": "Primary hypercholesterolemia (familial hypercholesterolemia — FH, often very high LDL), secondary: hypothyroidism, diabetes, nephrotic syndrome, cholestasis, anorexia nervosa, medications (steroids, thiazides, retinoids), high saturated/trans fat diet.",
            "effects": "Accelerated atherosclerosis: coronary artery disease, stroke, peripheral arterial disease. Xanthelasma (periorbital deposits), xanthomas (tendinous in FH). Pancreatitis risk (very high triglycerides contributing to total cholesterol).",
            "solution": "Cardiovascular risk assessment (Framingham, SCORE, ACC/AHA Pooled Cohort Equations). Lifestyle modification: heart-healthy diet (Mediterranean diet, reduced saturated fat, increased fiber), aerobic exercise (150 min/week), weight loss. Pharmacotherapy: statins (first-line — high-intensity for high-risk patients), ezetimibe (add-on), PCSK9 inhibitors (alirocumab, evolocumab — for FH or statin-intolerant), fibrates (for hypertriglyceridemia)."
        },
        "Normal": {
            "meaning": "Total cholesterol below 200 mg/dL is considered desirable, reflecting lower cardiovascular risk in most population-based risk models.",
            "causes": "N/A - This is a normal result.",
            "effects": "Reduced atherosclerotic cardiovascular risk when combined with favorable HDL and LDL levels.",
            "solution": "Maintain healthy diet (low in saturated fat, high in fiber and omega-3), regular physical activity. Annual lipid panel after age 35 (men) or 45 (women), or earlier with risk factors."
        }
    },

    "hdl_cholesterol": {
        "Low": {
            "meaning": "HDL below 40 mg/dL (men) or 50 mg/dL (women) is a significant independent cardiovascular risk factor; HDL participates in reverse cholesterol transport, removing cholesterol from arterial walls.",
            "causes": "Physical inactivity, obesity, smoking, type 2 diabetes and insulin resistance, metabolic syndrome, high carbohydrate diet, hypertriglyceridemia, medications (beta-blockers, thiazides, anabolic steroids, progestins), genetic hypoalphalipoproteinemia, Tangier disease.",
            "effects": "Accelerated atherogenesis, increased ASCVD risk (CAD, stroke, PAD). Low HDL is the most common lipid abnormality in coronary artery disease patients.",
            "solution": "Aerobic exercise (most effective intervention — raises HDL 5–10%): 150 min/week moderate intensity. Smoking cessation (raises HDL by 4 mg/dL). Niacin (most potent HDL raiser, but cardiovascular outcomes benefit not proven in trials on top of statin). Fibrates and omega-3s modestly raise HDL. Weight loss, alcohol moderation (1 drink/day increases HDL). HDL-raising medications have not consistently demonstrated CV outcome benefit — target LDL remains primary."
        },
        "High": {
            "meaning": "HDL above 60 mg/dL is generally considered protective; however, very high HDL (above 80 mg/dL) may paradoxically be associated with increased mortality in some populations (dysfunctional HDL).",
            "causes": "Regular aerobic exercise, moderate alcohol consumption (mechanism includes CETP inhibition), genetic hyperalphalipoproteinemia, medications (estrogen, fibrates, niacin), CETP deficiency (genetic).",
            "effects": "Generally protective against ASCVD. Very high HDL (>100 mg/dL): potential dysfunctional HDL with pro-inflammatory properties; paradoxical ASCVD risk in some studies.",
            "solution": "Maintain lifestyle factors that physiologically raise HDL (exercise, healthy diet). Very high HDL alone does not guarantee CV protection — evaluate full risk profile. CETP inhibitors (anacetrapib, evacetrapib) dramatically raised HDL but did not improve CV outcomes."
        },
        "Normal": {
            "meaning": "HDL 40–60 mg/dL (men) or 50–60 mg/dL (women) supports reverse cholesterol transport and provides moderate cardiovascular protection.",
            "causes": "N/A - This is a normal result.",
            "effects": "Moderate capacity for reverse cholesterol transport from peripheral tissues.",
            "solution": "Regular physical activity, maintain healthy weight, avoid smoking to optimize HDL. HDL above 60 mg/dL is a negative risk factor in Framingham risk scoring (reduces overall risk)."
        }
    },

    "ldl_cholesterol": {
        "Low": {
            "meaning": "LDL below 70 mg/dL is the treatment target for very high cardiovascular risk patients (e.g., established ASCVD, FH with prior MI). Very low LDL from statins is generally safe.",
            "causes": "High-intensity statin therapy, PCSK9 inhibitors, bempedoic acid, mipomersen, lomitapide (for homozygous FH), abetalipoproteinemia (genetic).",
            "effects": "In patients on therapy: desired outcome — reduced ASCVD events. Concerns about very low LDL (<25 mg/dL) from genetic variants: possible association with hemorrhagic stroke and diabetes — current evidence insufficient to limit pharmacological LDL lowering.",
            "solution": "Continue therapeutic LDL lowering per guidelines. For patients on statins: LDL <70 mg/dL is appropriate for very high-risk patients; <55 mg/dL for extreme risk (recurrent MI, polyvascular disease)."
        },
        "High": {
            "meaning": "LDL cholesterol is the primary causal factor in atherosclerotic cardiovascular disease (ASCVD). LDL >100 mg/dL requires evaluation and management based on total cardiovascular risk.",
            "causes": "High saturated fat/trans fat diet, familial hypercholesterolemia (FH — autosomal dominant, extremely high LDL from birth), hypothyroidism, nephrotic syndrome, liver disease, diabetes, medications (corticosteroids, anabolic steroids, ciclosporin), obesity.",
            "effects": "Plaque deposition in coronary arteries, carotid arteries, peripheral arteries — leading to angina, MI, stroke, TIA, intermittent claudication, aortic stenosis. Tendon xanthomas (FH), corneal arcus, xanthelasma.",
            "solution": "Cardiovascular risk stratification. Optimal LDL targets: <100 mg/dL (high risk), <70 mg/dL (very high risk: established ASCVD, FH with prior event), <55 mg/dL (extreme risk). Statins (atorvastatin 40–80 mg, rosuvastatin 20–40 mg first-line). Add ezetimibe if LDL target not reached. PCSK9 inhibitors (alirocumab, evolocumab) for high-risk patients not at goal with statins. Inclisiran (siRNA), bempedoic acid for additional options."
        },
        "Normal": {
            "meaning": "LDL cholesterol below 100 mg/dL is considered optimal for most adults; below 70 mg/dL is optimal for those with established heart disease.",
            "causes": "N/A - This is a normal result.",
            "effects": "Reduced atherosclerotic plaque formation risk.",
            "solution": "Maintain heart-healthy diet (Mediterranean diet), regular exercise, non-smoking. Annual lipid screening. In established CVD patients, LDL <70 mg/dL is the target regardless of baseline."
        }
    },

    "triglycerides": {
        "Low": {
            "meaning": "Triglycerides below 50 mg/dL are uncommon and may occur with very low carbohydrate (ketogenic) diet, hyperthyroidism, or abetalipoproteinemia.",
            "causes": "Ketogenic/very low carbohydrate diet, hyperthyroidism, abetalipoproteinemia, malnutrition.",
            "effects": "Very low triglycerides themselves are not harmful; clinical features are from the underlying condition.",
            "solution": "No specific intervention for low triglycerides. Evaluate underlying cause if unexpected."
        },
        "High": {
            "meaning": "Triglycerides: 150–199 mg/dL: borderline; 200–499 mg/dL: high; ≥500 mg/dL: very high (significant pancreatitis risk); ≥1,000 mg/dL: severe (high pancreatitis risk).",
            "causes": "Secondary (most common): type 2 diabetes, obesity, metabolic syndrome, excessive alcohol, high carbohydrate/sugar diet, hypothyroidism, CKD, nephrotic syndrome, medications (steroids, thiazides, beta-blockers, retinoids, estrogen, antipsychotics). Primary: familial hypertriglyceridemia, familial combined hyperlipidemia, lipoprotein lipase deficiency (rare — chylomicronemia).",
            "effects": "Pancreatitis risk (≥500 mg/dL — abdominal pain, nausea, vomiting, elevated lipase, amylase). Cardiovascular risk (moderate elevation). Eruptive xanthomas (chylomicronemia). Lipemia retinalis (whitish retinal vessels — very high TGs). Hepatosplenomegaly.",
            "solution": "Treat underlying condition (diabetes, hypothyroidism, alcohol cessation, medication review). Dietary modification: reduce refined carbohydrates, sugars, alcohol. Weight loss. Exercise. Pharmacotherapy for TGs >500 mg/dL: fibrates (fenofibrate — first-line), omega-3 fatty acids (icosapentaenoic acid — REDUCE-IT trial showed CV benefit at 4 g/day), niacin. Target TGs <150 mg/dL; for pancreatitis prevention when >500: target <500 urgently."
        },
        "Normal": {
            "meaning": "Triglycerides below 150 mg/dL indicates normal VLDL metabolism and carbohydrate-to-fat conversion.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal energy storage lipid transport without chylomicronemia or pancreatitis risk.",
            "solution": "Maintain low-sugar, low-refined-carbohydrate diet. Regular exercise. Moderate alcohol intake (<1–2 drinks/day). Annual lipid panel."
        }
    },

    # ==========================================================================
    # SECTION 7: CARDIAC MARKER TESTS
    # ==========================================================================

    "troponin_i": {
        "Low": {
            "meaning": "Undetectable or below the limit of detection for high-sensitivity troponin I effectively rules out myocardial injury in the appropriate clinical context.",
            "causes": "Absence of myocardial cell necrosis or significant damage.",
            "effects": "HEART score and clinical assessment used to determine further management. Negative high-sensitivity troponin at 0 and 3 hours rules out NSTEMI with very high negative predictive value (>99%).",
            "solution": "In low-risk ACS patients with negative serial troponin: discharge with outpatient follow-up and stress testing. Continue risk factor management."
        },
        "High": {
            "meaning": "Elevated cardiac troponin I (above the 99th percentile of a reference population) indicates myocardial cell injury and necrosis — the cornerstone of acute myocardial infarction diagnosis when combined with clinical symptoms and ECG changes.",
            "causes": "Type 1 MI: atherosclerotic plaque rupture and coronary thrombosis. Type 2 MI: myocardial oxygen demand-supply mismatch (tachyarrhythmia, severe anemia, hypotension, hypertensive crisis). Non-ischemic cardiac injury: myocarditis, cardiac contusion, heart failure (both acute and chronic), cardiac ablation or cardioversion. Non-cardiac causes: pulmonary embolism (RV strain), sepsis, rhabdomyolysis, acute neurological events (SAH), acute kidney injury, COPD exacerbation.",
            "effects": "Myocardial cell death, ventricular dysfunction, arrhythmias, cardiogenic shock, heart failure, sudden cardiac death. Troponin elevation correlates with infarct size and prognosis.",
            "solution": "Immediate 12-lead ECG. STEMI: primary percutaneous coronary intervention (PCI) within 90 minutes (or fibrinolysis if PCI unavailable). NSTEMI: anticoagulation (heparin/LMWH), dual antiplatelet therapy (aspirin + ticagrelor or prasugrel), early invasive strategy within 24 hours for high-risk NSTEMI (recurrent chest pain, hemodynamic instability, elevated troponin). Long-term: beta-blockers, ACE inhibitors/ARBs, statin, aspirin, P2Y12 inhibitor for 12 months post-MI."
        },
        "Normal": {
            "meaning": "Troponin I below the 99th percentile upper reference limit in the appropriate clinical setting and timing effectively rules out acute MI.",
            "causes": "N/A - This is a normal result.",
            "effects": "No detectable myocardial cell necrosis.",
            "solution": "Serial troponin measurement at 0, 3, and 6 hours for suspected ACS (if initial troponin negative). Consider alternative diagnosis for chest pain (aortic dissection, PE, pericarditis, costochondritis). Assess pre-test probability and HEART score."
        }
    },

    "ck_mb": {
        "Low": {
            "meaning": "CK-MB below 5 ng/mL or below 3–5% of total CK indicates no significant cardiac muscle damage.",
            "causes": "Normal cardiac enzyme activity, absence of myocardial injury.",
            "effects": "No evidence of myocardial infarction.",
            "solution": "CK-MB has largely been replaced by high-sensitivity troponin for MI diagnosis. Use troponin as primary cardiac biomarker."
        },
        "High": {
            "meaning": "Elevated CK-MB (above 5% of total CK or above laboratory-specific cutoff) indicates myocardial muscle cell damage, historically important for MI diagnosis, now supplementary to troponin.",
            "causes": "Acute MI (peaks at 18–24 hours, returns to normal by 36–48 hours — useful for detecting re-infarction when troponin remains elevated), myocarditis, cardiac surgery/ablation, cardioversion (minor), rhabdomyolysis (CK-MB may be elevated as skeletal muscle contains trace CK-MB).",
            "effects": "Myocardial necrosis, pump failure, arrhythmias.",
            "solution": "Troponin is preferred for initial MI diagnosis. CK-MB useful for diagnosing re-infarction (as it returns to baseline faster than troponin). ECG-guided management as for MI. Monitor for complications (arrhythmias, heart failure)."
        },
        "Normal": {
            "meaning": "CK-MB within normal range confirms no significant cardiac muscle damage.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal cardiac sarcolemmal integrity.",
            "solution": "Serial troponin remains the gold standard for ACS rule-out. CK-MB monitoring post-cardiac surgery for early re-infarction detection."
        }
    },

    "bnp": {
        "Low": {
            "meaning": "BNP below 35–100 pg/mL (lab-dependent) effectively rules out significant heart failure in dyspneic patients.",
            "causes": "Normal ventricular wall stress, absence of significant ventricular volume/pressure overload.",
            "effects": "Heart failure is very unlikely in dyspneic patients with normal BNP — negative predictive value >95%.",
            "solution": "Pursue alternative diagnoses for dyspnea (COPD, PE, pneumonia, anemia, pulmonary hypertension). No heart failure treatment indicated."
        },
        "High": {
            "meaning": "BNP above 400 pg/mL (NT-proBNP >900 pg/mL) strongly suggests heart failure; intermediate values require clinical context. Secreted by ventricular cardiomyocytes in response to increased wall stress.",
            "causes": "Heart failure (primary indicator — correlates with NYHA class and prognosis), acute decompensated heart failure, left ventricular dysfunction (systolic or diastolic), pulmonary hypertension (RV strain), pulmonary embolism (acute RV overload), atrial fibrillation, AKI/CKD (impaired clearance — particularly for NT-proBNP), sepsis, cardiac tamponade.",
            "effects": "Dyspnea (orthopnea, paroxysmal nocturnal dyspnea), ankle edema, fatigue, reduced exercise tolerance, elevated JVP, S3 gallop, pulmonary crackles.",
            "solution": "Heart failure confirmed: diuretics (furosemide — for acute decongestion), ACEI/ARB/ARNI (sacubitril/valsartan — LCZ696), beta-blockers (carvedilol, bisoprolol, metoprolol succinate), aldosterone antagonists (spironolactone/eplerenone), SGLT2 inhibitors (dapagliflozin, empagliflozin — new 4th pillar of HFrEF treatment). ICD/CRT for eligible patients. Serial BNP monitoring guides decongestion therapy."
        },
        "Normal": {
            "meaning": "BNP below 100 pg/mL makes heart failure unlikely in the differential of dyspnea.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal ventricular wall stress and filling pressures.",
            "solution": "In patients with established HF, normal BNP on therapy indicates good treatment response. Continue guideline-directed medical therapy."
        }
    },

    "homocysteine": {
        "Low": {
            "meaning": "Homocysteine below normal has no known clinical significance.",
            "causes": "Adequate folate, B12, and B6 status, healthy dietary habits.",
            "effects": "No adverse effects from low homocysteine.",
            "solution": "No action required."
        },
        "High": {
            "meaning": "Elevated homocysteine (above 15 µmol/L — hyperhomocysteinemia) is an independent cardiovascular risk factor and associated with thrombosis, renal disease, and cognitive decline.",
            "causes": "B12 deficiency, folate deficiency, pyridoxine (B6) deficiency (homocysteine metabolism requires all three vitamins), homocystinuria (severe — CBS enzyme defect), CKD (reduced excretion), hypothyroidism, medications (methotrexate — antifolate, theophylline), aging, smoking, genetic polymorphisms (MTHFR C677T).",
            "effects": "Premature atherosclerosis, thromboembolism (both venous and arterial), stroke, cognitive decline, dementia, osteoporosis. Homocystinuria: Marfanoid habitus, ectopia lentis, intellectual disability, thromboembolism, premature atherosclerosis in children.",
            "solution": "Supplement folic acid (0.4–5 mg/day), B12, and B6. Supplementation effectively lowers homocysteine but randomized trials have not consistently shown reduction in cardiovascular events — homocysteine may be a marker rather than a cause. Treat underlying B12/folate deficiency, hypothyroidism, CKD. For homocystinuria: low methionine diet, high-dose pyridoxine (pyridoxine-responsive form), betaine."
        },
        "Normal": {
            "meaning": "Homocysteine 5–15 µmol/L reflects adequate methionine remethylation and transsulfuration pathways, supported by sufficient B vitamins.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal methionine metabolism without endothelial toxicity.",
            "solution": "Maintain adequate folate (dark leafy greens), B12 (animal products), B6 (poultry, fish, potatoes) intake. Screening for high-risk individuals (family history of premature CVD, CKD)."
        }
    },

    # ==========================================================================
    # SECTION 8: THYROID FUNCTION TESTS
    # ==========================================================================

    "tsh": {
        "Low": {
            "meaning": "TSH below 0.4 mIU/L indicates suppressed pituitary TSH secretion, most commonly reflecting hyperthyroidism (excessive thyroid hormone feedback) or exogenous thyroid hormone excess.",
            "causes": "Primary hyperthyroidism: Graves' disease (most common), toxic multinodular goiter, toxic adenoma, thyroiditis (subacute De Quervain's, silent, postpartum — transient hyperthyroid phase), iodine excess (Jod-Basedow phenomenon), thyroid carcinoma (rarely). Exogenous: over-replacement with levothyroxine, intentional TSH suppression in thyroid cancer follow-up. Non-thyroidal: severe non-thyroidal illness (euthyroid sick syndrome), steroids, dopamine infusion, central hypothyroidism (TSH inappropriately low with low T4).",
            "effects": "Suppressed TSH alone (subclinical hyperthyroidism): atrial fibrillation risk, osteoporosis (particularly in post-menopausal women), cardiac adverse effects. Overt hyperthyroidism: palpitations, tachycardia, atrial fibrillation, anxiety, tremor, weight loss despite increased appetite, heat intolerance, sweating, diarrhea, insomnia, proptosis and lid lag (Graves' ophthalmopathy), thyroid bruit, fine hair, onycholysis, pretibial myxedema (Graves').",
            "solution": "Confirm with Free T4, Free T3. Graves' disease: antithyroid drugs (methimazole/carbimazole — first-line), radioiodine ablation (I-131), thyroidectomy. Beta-blockers (propranolol) for symptom control. Toxic nodule: radioiodine or surgery. Transient thyroiditis: supportive (beta-blockers), NSAIDs for pain. Adjust levothyroxine dose if iatrogenic."
        },
        "High": {
            "meaning": "TSH above 4.5 mIU/L indicates primary hypothyroidism — increased pituitary TSH secretion in response to inadequate thyroid hormone production.",
            "causes": "Hashimoto's thyroiditis (autoimmune — most common cause in iodine-replete areas), iodine deficiency (most common cause globally), post-radioiodine or thyroidectomy, medications (amiodarone, lithium, interferon-alpha, tyrosine kinase inhibitors), congenital hypothyroidism, subacute thyroiditis (recovery phase), infiltrative disease (sarcoidosis, amyloidosis).",
            "effects": "Subclinical hypothyroidism (high TSH, normal FT4): mild fatigue, weight gain, dyslipidemia, possible cardiovascular risk. Overt hypothyroidism: fatigue, cold intolerance, constipation, weight gain, bradycardia, dry skin, hair loss, hoarseness, periorbital puffiness, cognitive slowing, depression, menstrual irregularities, hyperlipidemia, carpal tunnel syndrome, myopathy. Severe: myxedema coma (life-threatening).",
            "solution": "Overt hypothyroidism: levothyroxine (T4) replacement — start 1.6 µg/kg/day (lower dose in elderly/cardiac disease). Monitor TSH every 6–8 weeks and adjust dose to maintain TSH 0.5–2.5 mIU/L. Subclinical hypothyroidism: treat if TSH >10 mIU/L, if symptomatic, or in pregnancy (TSH >2.5 mIU/L). Myxedema coma: IV T4 + T3, hydrocortisone (exclude adrenal insufficiency), warm slowly, ICU."
        },
        "Normal": {
            "meaning": "TSH 0.4–4.5 mIU/L (tighter range in pregnancy: 0.1–2.5 mIU/L in first trimester) indicates normal hypothalamic-pituitary-thyroid axis feedback.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal thyroid hormone production and appropriate metabolic regulation.",
            "solution": "TSH is the most sensitive initial thyroid screening test. Screen every 5 years after age 35 (especially women). Annual testing for patients on levothyroxine. Pregnancy: test TSH as soon as pregnancy confirmed."
        }
    },

    "free_t4": {
        "Low": {
            "meaning": "Free T4 (FT4) below 0.8 ng/dL with elevated TSH confirms overt primary hypothyroidism. Low FT4 with low/normal TSH suggests central (secondary) hypothyroidism.",
            "causes": "Primary hypothyroidism (Hashimoto's, post-thyroidectomy, radioiodine, iodine deficiency). Central: pituitary disease (adenoma, Sheehan's syndrome), hypothalamic disease.",
            "effects": "Hypothyroid manifestations as listed under TSH. Central hypothyroidism: less severe symptoms, associated with other pituitary hormone deficiencies.",
            "solution": "Primary hypothyroidism: levothyroxine as described. Central hypothyroidism: must exclude adrenal insufficiency and treat with hydrocortisone BEFORE levothyroxine (to prevent precipitating Addisonian crisis). Pituitary MRI. Full pituitary function testing."
        },
        "High": {
            "meaning": "Elevated FT4 with suppressed TSH confirms overt hyperthyroidism. Elevated FT4 with elevated TSH suggests TSH-secreting pituitary adenoma.",
            "causes": "Graves' disease, toxic nodule/goiter, exogenous T4 intake, thyroiditis (subacute), iodine excess, amiodarone (contains 37% iodine), factitious thyrotoxicosis (T4 ingestion), struma ovarii.",
            "effects": "Hyperthyroid symptoms: palpitations, tremor, weight loss, heat intolerance, anxiety, thyroid storm (life-threatening acute decompensation — fever, cardiovascular collapse, encephalopathy).",
            "solution": "Antithyroid drugs, beta-blockers, radioiodine, or thyroidectomy depending on etiology. Thyroid storm: methimazole (or PTU) + beta-blocker + Lugol's iodine + corticosteroids + intensive supportive care."
        },
        "Normal": {
            "meaning": "FT4 within 0.8–1.8 ng/dL with normal TSH confirms euthyroid state.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal thyroid hormone-mediated regulation of metabolism, growth, cardiovascular function, and neurodevelopment.",
            "solution": "Routine screening. No levothyroxine adjustment needed if TSH and FT4 are both normal."
        }
    },

    "anti_tpo": {
        "Low": {
            "meaning": "Negative Anti-TPO antibodies indicate absence of detectable thyroid autoimmunity.",
            "causes": "No autoimmune thyroid disease. Normal immune tolerance to thyroid peroxidase.",
            "effects": "No evidence of autoimmune thyroid destruction.",
            "solution": "No specific action. If hypothyroidism is present with negative Anti-TPO, consider non-autoimmune causes (iodine deficiency, medications, infiltrative disease)."
        },
        "High": {
            "meaning": "Elevated Anti-TPO antibodies confirm thyroid autoimmunity, most commonly Hashimoto's thyroiditis or Graves' disease, indicating autoimmune thyroid gland attack.",
            "causes": "Hashimoto's thyroiditis (chronic autoimmune hypothyroidism — most common), Graves' disease, postpartum thyroiditis, subacute lymphocytic (silent) thyroiditis. Also present in 10% of normal individuals (especially post-menopausal women) without thyroid dysfunction.",
            "effects": "Progressive thyroid destruction (Hashimoto's) leading to hypothyroidism. Pregnant women with positive Anti-TPO have higher risk of postpartum thyroiditis and fetal hypothyroidism. Association with other autoimmune conditions (type 1 diabetes, rheumatoid arthritis, Addison's disease).",
            "solution": "Monitor TSH every 6–12 months in Anti-TPO positive euthyroid individuals. Levothyroxine when TSH rises above 10 mIU/L or if symptomatic. Selenium supplementation (200 µg/day) may reduce Anti-TPO levels in Hashimoto's thyroiditis (benefit on disease progression less clear). Screen for other autoimmune conditions."
        },
        "Normal": {
            "meaning": "Anti-TPO within normal limits (negative) indicates no detectable anti-thyroid peroxidase autoimmunity.",
            "causes": "N/A - This is a normal result.",
            "effects": "Absence of ongoing autoimmune attack on thyroid gland.",
            "solution": "Reassuring in the setting of thyroid dysfunction — non-autoimmune causes should be explored. No specific monitoring for Anti-TPO beyond routine TSH screening."
        }
    },

    # ==========================================================================
    # SECTION 9: HORMONAL / ENDOCRINE TESTS
    # ==========================================================================

    "testosterone": {
        "Low": {
            "meaning": "Total testosterone below 300 ng/dL (men) indicates hypogonadism — insufficient androgen production. In women, low testosterone has less well-defined clinical significance.",
            "causes": "Primary hypogonadism (testicular failure): Klinefelter's syndrome (47,XXY), orchitis (mumps, autoimmune), cryptorchidism, chemotherapy, radiation, trauma, castration. Secondary hypogonadism (pituitary/hypothalamic failure): hyperprolactinemia, pituitary adenoma, Kallmann's syndrome, obesity (functional), systemic illness, medications (opioids, glucocorticoids, anabolic steroids — negative feedback), aging (late-onset hypogonadism).",
            "effects": "Reduced libido, erectile dysfunction, decreased muscle mass, increased body fat, fatigue, depressed mood, osteoporosis, infertility, gynecomastia, reduced facial/body hair, anemia (mild), cognitive decline in severe cases.",
            "solution": "Confirm with repeat morning testosterone (diurnal variation) plus LH and FSH. Primary: high LH/FSH + low T. Secondary: low/normal LH/FSH + low T. Testosterone replacement therapy (TRT): intramuscular (cypionate/enanthate), transdermal (gel/patch), subcutaneous pellets — if hypogonadism is confirmed and symptomatic. Monitor prostate, hematocrit, lipids. Fertility-preserving options (clomiphene, gonadotropins) if fertility desired."
        },
        "High": {
            "meaning": "Elevated testosterone in men may indicate exogenous administration; in women, elevated testosterone indicates androgen excess — clinically significant.",
            "causes": "Men: anabolic steroid abuse, testosterone replacement (supraphysiologic dosing), adrenocortical carcinoma, testicular tumor (Leydig cell tumor — very high testosterone), congenital adrenal hyperplasia (CAH). Women: PCOS (most common), congenital adrenal hyperplasia, ovarian or adrenal androgen-secreting tumor, exogenous androgen use.",
            "effects": "Men with exogenous testosterone: testicular atrophy (suppressed LH/FSH), polycythemia, sleep apnea, hypertension, dyslipidemia, infertility. Women: hirsutism, acne, oligomenorrhea/amenorrhea, clitoromegaly, alopecia (male-pattern), deepening voice, virilization in severe cases (tumor). PCOS: anovulation, infertility, metabolic syndrome, insulin resistance.",
            "solution": "Women: PCOS management (lifestyle modification, metformin, combined oral contraceptives for cycle regulation and anti-androgen effect, spironolactone for hirsutism). Ovarian/adrenal tumor: urgent surgical referral. CAH: corticosteroid suppression (hydrocortisone/dexamethasone). Stop anabolic steroid abuse."
        },
        "Normal": {
            "meaning": "Testosterone within normal range (300–1,000 ng/dL in men; 15–70 ng/dL in women) indicates normal gonadal hormone production.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal libido, muscle mass maintenance, bone density, erythropoiesis, and mood regulation.",
            "solution": "Maintain healthy weight (obesity reduces testosterone), regular exercise (resistance training increases testosterone), adequate sleep, stress management."
        }
    },

    "prolactin": {
        "Low": {
            "meaning": "Prolactin below normal has no established clinical significance in non-lactating individuals.",
            "causes": "Sheehan's syndrome (postpartum pituitary infarction), hypopituitarism, medications (cabergoline, bromocriptine — therapeutic), rare pituitary failure.",
            "effects": "Postpartum hypoprolactinemia (Sheehan's): inability to lactate. Associated hypopituitarism effects (growth hormone deficiency, hypogonadism, hypothyroidism, adrenal insufficiency).",
            "solution": "Assess full pituitary function in suspected pituitary failure. MRI pituitary. Hormone replacement for each deficient axis."
        },
        "High": {
            "meaning": "Elevated prolactin (above 25 ng/mL in non-pregnant women, >17 ng/mL in men, physiologically high in pregnancy and lactation) — hyperprolactinemia — suppresses the hypothalamic-pituitary-gonadal axis.",
            "causes": "Physiological: pregnancy, breastfeeding, stress, sleep, nipple stimulation. Pathological: prolactinoma (most common pituitary adenoma — microprolactinoma <10mm, macroprolactinoma >10mm), medications (dopamine antagonists: antipsychotics/haloperidol/risperidone, metoclopramide, domperidone; antidepressants; verapamil; opioids; H2 blockers), primary hypothyroidism (TRH stimulates prolactin), CKD (reduced clearance), chest wall trauma/surgery, pituitary stalk compression by any pituitary/hypothalamic lesion.",
            "exploitation": "Galactorrhea (inappropriate milk production), amenorrhea, oligomenorrhea, infertility (in women); in men: decreased libido, erectile dysfunction, infertility, hypogonadism, rarely gynecomastia/galactorrhea. Macroprolactinoma: headaches, visual field defects (bitemporal hemianopia — chiasm compression), hypopituitarism.",
            "solution": "Exclude physiological and drug causes first. MRI pituitary with gadolinium for all persistent hyperprolactinemia. Microprolactinoma: dopamine agonists (cabergoline — first-line; bromocriptine). Macroprolactinoma: cabergoline; surgery (transsphenoidal) if resistant or visual field deficit persists. Discontinue offending medication if drug-induced and substitute."
        },
        "Normal": {
            "meaning": "Prolactin within normal range indicates appropriate dopaminergic inhibition of pituitary lactotrophs without pathological excess.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal reproductive hormone axis function; lactation appropriately initiated only in pregnancy/postpartum.",
            "solution": "Measure fasting, morning prolactin to avoid stress-related elevation. Macroprolactin screening (polyethylene glycol precipitation) if clinical features absent with mildly elevated prolactin."
        }
    },

    "cortisol": {
        "Low": {
            "meaning": "8 AM serum cortisol below 3 µg/dL is highly suggestive of adrenal insufficiency; confirmed by ACTH stimulation test.",
            "causes": "Primary adrenal insufficiency (Addison's disease): autoimmune (most common in developed countries), tuberculosis (most common globally), adrenal hemorrhage (Waterhouse-Friderichsen syndrome in meningococcemia), HIV/CMV adrenalitis, bilateral adrenalectomy, adrenal metastases. Secondary: pituitary failure (Sheehan's, hypophysitis, adenoma), prolonged exogenous corticosteroid therapy causing HPA axis suppression, hypothalamic disease. Tertiary: hypothalamic CRH deficiency.",
            "effects": "Chronic: fatigue, weakness, anorexia, weight loss, hyperpigmentation (primary only — high ACTH), nausea, abdominal pain, postural hypotension, hyponatremia, hyperkalemia (primary only — mineralocorticoid deficiency), hypoglycemia. Acute (Addisonian crisis): severe hypotension, collapse, electrolyte crisis — life-threatening medical emergency.",
            "solution": "Addisonian crisis: immediate IV hydrocortisone 100 mg bolus then 50–100 mg 6-hourly, IV normal saline + dextrose, treat precipitating cause. Chronic replacement: hydrocortisone 15–25 mg/day in divided doses (mimics diurnal rhythm) ± fludrocortisone 50–200 µg/day for primary. Sick day rules: double/triple hydrocortisone dose during illness. Medical alert bracelet."
        },
        "High": {
            "meaning": "Elevated cortisol, particularly with loss of diurnal variation, suggests Cushing's syndrome (endogenous cortisol excess) or exogenous glucocorticoid use.",
            "causes": "ACTH-dependent: pituitary corticotroph adenoma (Cushing's disease — 70% of endogenous cases), ectopic ACTH secretion (small cell lung cancer, carcinoid, medullary thyroid carcinoma). ACTH-independent: adrenal adenoma, adrenal carcinoma, bilateral adrenal hyperplasia. Pseudo-Cushing's: major depression, alcohol use disorder (alcoholic pseudo-Cushing's), poorly controlled diabetes, obesity. Iatrogenic: most common — exogenous corticosteroid use.",
            "effects": "Central obesity (buffalo hump, truncal fat), facial fullness (moon face), purple striae, proximal muscle weakness, hirsutism, thin skin and bruising, hypertension, hyperglycemia/diabetes, osteoporosis, pathological fractures, secondary immunosuppression (recurrent infections), psychiatric disturbances (depression, psychosis), menstrual irregularities, growth retardation in children.",
            "solution": "Confirm with 24-hour urine free cortisol, late-night salivary cortisol, and/or 1 mg overnight dexamethasone suppression test. ACTH level to determine cause. Pituitary MRI, CT chest/abdomen for ectopic ACTH. Surgery: transsphenoidal adenomectomy (Cushing's disease), adrenalectomy (adrenal tumor). Medical: steroidogenesis inhibitors (metyrapone, ketoconazole, osilodrostat, mitotane). Taper exogenous steroids if iatrogenic."
        },
        "Normal": {
            "meaning": "Morning cortisol 5–25 µg/dL with preserved diurnal variation (higher AM, lower PM/midnight) indicates normal HPA axis function.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal stress response, immune modulation, glucose regulation, and circadian rhythm.",
            "solution": "Diurnal variation is essential for healthy physiology. Protect sleep-wake cycle and circadian rhythm to support cortisol rhythm. Testing must be done at 8 AM fasting."
        }
    },

    "lh": {
        "Low": {
            "meaning": "LH below normal indicates suppression of the hypothalamic-pituitary-gonadal axis, causing secondary hypogonadism.",
            "causes": "Hyperprolactinemia (most common — prolactin suppresses GnRH), Kallmann syndrome (congenital GnRH deficiency), pituitary adenoma, severe systemic illness, extreme weight loss/anorexia nervosa, excessive exercise (athlete's triad), exogenous anabolic steroids/testosterone (feedback suppression), opioid use, Sheehan's syndrome.",
            "effects": "Women: amenorrhea, anovulation, infertility, low estrogen (vaginal dryness, hot flashes, osteoporosis). Men: decreased testosterone (low libido, ED), azoospermia, infertility.",
            "solution": "Treat underlying cause (correct prolactin, stop offending drugs, nutrition rehabilitation). For fertility: gonadotropin therapy (FSH + LH/hCG or GnRH pump). GnRH agonist or kisspeptin therapy for Kallmann syndrome. Pituitary tumor management."
        },
        "High": {
            "meaning": "Elevated LH with low sex hormones indicates primary gonadal failure (hypergonadotropic hypogonadism) — the pituitary is trying to compensate for absent gonadal hormone production.",
            "causes": "Women: primary ovarian insufficiency (POI)/premature ovarian failure (autoimmune, Turner syndrome 45,X, chemotherapy, radiation, idiopathic), menopause. Men: Klinefelter syndrome, orchitis (mumps), bilateral torsion, chemotherapy, radiation, testicular agenesis.",
            "effects": "Women: amenorrhea, infertility, hot flashes, osteoporosis, cardiovascular risk from prolonged estrogen deficiency. Men: hypogonadism symptoms, infertility.",
            "solution": "Hormone replacement therapy: estrogen + progesterone in POI women (until natural menopause age). Testosterone replacement for men with primary hypogonadism. IVF with donor eggs for POI women desiring fertility. Karyotype (Turner syndrome), anti-Müllerian hormone (ovarian reserve)."
        },
        "Normal": {
            "meaning": "LH within normal range indicates normal hypothalamic-pituitary-gonadal axis signaling.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal cyclic ovulation in women; normal testosterone production in men.",
            "solution": "LH measured on Day 3 of cycle for baseline reproductive assessment. LH surge detection (mid-cycle, Day 12–14) used for ovulation timing."
        }
    },

    "fsh": {
        "Low": {
            "meaning": "Low FSH with low sex hormones indicates secondary (central) hypogonadism — inadequate pituitary FSH secretion.",
            "causes": "Hyperprolactinemia, hypothalamic dysfunction (anorexia, excessive exercise), pituitary disease, exogenous steroid use, GnRH analogue therapy.",
            "effects": "Women: anovulation, infertility, amenorrhea, low estrogen effects. Men: impaired spermatogenesis, infertility.",
            "solution": "Treat underlying cause. Gonadotropin therapy with recombinant FSH (follitropin) for ovarian stimulation. GnRH pulse therapy for hypothalamic hypogonadism."
        },
        "High": {
            "meaning": "Elevated FSH indicates primary gonadal failure or menopause (in women). FSH >40 mIU/mL in a reproductive-age woman with amenorrhea confirms premature ovarian insufficiency.",
            "causes": "Menopause (physiological), premature ovarian insufficiency (POI), Turner syndrome, chemotherapy/radiation, ovarian dysgenesis. Men: primary testicular failure (Klinefelter's, orchitis), azoospermia due to spermatogenic failure.",
            "effects": "Women: infertility, menopausal symptoms, osteoporosis risk. Men: azoospermia, infertility.",
            "solution": "POI: hormone replacement therapy (estrogen + progesterone). Fertility treatment with donor oocytes for POI. Men with high FSH and azoospermia: testicular sperm extraction (TESE) for ICSI."
        },
        "Normal": {
            "meaning": "FSH within normal range indicates adequate gonadotropin signaling for gametogenesis and sex hormone production.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal folliculogenesis (women) and spermatogenesis (men).",
            "solution": "FSH measured on Day 2–3 of cycle for ovarian reserve assessment. FSH >10 mIU/mL on Day 3 may indicate diminished ovarian reserve."
        }
    },

    "pth": {
        "Low": {
            "meaning": "PTH below 15 pg/mL (hypoparathyroidism) indicates inadequate parathyroid gland function, leading to hypocalcemia and hyperphosphatemia.",
            "causes": "Post-thyroid or parathyroid surgery (most common), autoimmune hypoparathyroidism (isolated or as part of APS1 — autoimmune polyendocrinopathy), hypomagnesemia (suppresses PTH secretion and action), Wilson's disease, hemochromatosis, infiltrative disease, congenital (DiGeorge syndrome — chromosome 22q11 deletion).",
            "effects": "Hypocalcemia: tetany, perioral paresthesias, Trousseau's and Chvostek's signs, seizures, prolonged QT, cataracts, calcifications (basal ganglia in chronic hypoparathyroidism), cognitive impairment.",
            "solution": "Treat hypocalcemia (as above). Oral calcium carbonate and active vitamin D (calcitriol) — standard management. Recombinant PTH (1–84) available for refractory cases. Correct hypomagnesemia. Calcium-sensing receptor agonist (cinacalcet) not applicable here. Lifelong supplementation with regular monitoring."
        },
        "High": {
            "meaning": "Elevated PTH causes hypercalcemia (primary hyperparathyroidism) or is an appropriate compensatory response to low calcium (secondary hyperparathyroidism in CKD/vitamin D deficiency).",
            "causes": "Primary hyperparathyroidism: parathyroid adenoma (85%), multiglandular disease (15%), parathyroid carcinoma (rare). Secondary: CKD (reduced calcitriol and calcium — PTH rises to compensate), vitamin D deficiency, malabsorption. Tertiary: secondary HPT that becomes autonomous after prolonged stimulation (after renal transplant).",
            "effects": "Primary HPT: hypercalcemia (bones, stones, groans, thrones, psychic overtones), nephrolithiasis, osteoporosis, osteitis fibrosa cystica (severe). Secondary HPT in CKD: renal osteodystrophy, vascular calcification, ectopic calcification.",
            "solution": "Primary HPT with symptoms or age <50: parathyroidectomy (curative). Surveillance for asymptomatic mild primary HPT meeting watchful waiting criteria. Medical: cinacalcet (lowers calcium in inoperable primary HPT). Secondary HPT: phosphate restriction, phosphate binders, calcitriol or vitamin D analogues (paricalcitol), calcimimetics (cinacalcet), parathyroidectomy for tertiary."
        },
        "Normal": {
            "meaning": "PTH 15–65 pg/mL ensures appropriate calcium-phosphate regulation through bone resorption, renal calcium retention, and intestinal calcium absorption (via vitamin D activation).",
            "causes": "N/A - This is a normal result.",
            "effects": "Stable serum calcium and phosphate; normal bone turnover.",
            "solution": "PTH should always be interpreted alongside serum calcium, phosphate, and vitamin D levels. Normal PTH with hypercalcemia: rule out non-PTH-mediated causes (malignancy, sarcoidosis, vitamin D toxicity)."
        }
    },

    "amh": {
        "Low": {
            "meaning": "Anti-Müllerian Hormone below 1.0 ng/mL indicates diminished ovarian reserve — fewer remaining ovarian follicles — associated with reduced fertility and earlier menopause.",
            "causes": "Advanced reproductive age (AMH declines with age), premature ovarian insufficiency (POI), previous ovarian surgery (cystectomy for endometrioma/dermoid), chemotherapy/radiation, endometriosis (severely affecting ovarian reserve), genetic factors, Turner syndrome.",
            "effects": "Poor ovarian response to gonadotropin stimulation in IVF, fewer eggs retrieved, lower IVF success rates, earlier menopause. Does not necessarily mean spontaneous conception is impossible if some follicles remain.",
            "solution": "Reproductive counseling — urgency if fertility desired. IVF with aggressive stimulation protocols (high gonadotropin doses). Oocyte or embryo cryopreservation before further ovarian damage (oncofertility). Donor oocyte IVF for very low reserves. Hormone replacement for POI."
        },
        "High": {
            "meaning": "Elevated AMH (above 3.5–5 ng/mL) indicates high ovarian follicle number, associated with PCOS or polycystic ovarian morphology.",
            "causes": "Polycystic ovary syndrome (PCOS — primary cause), polycystic ovarian morphology without full PCOS criteria, granulosa cell tumor of the ovary (markedly elevated — can use as tumor marker).",
            "effects": "PCOS: irregular periods, anovulation, infertility, hyperandrogenism (acne, hirsutism), insulin resistance. High AMH also means high risk of ovarian hyperstimulation syndrome (OHSS) during IVF stimulation.",
            "solution": "PCOS management: lifestyle modification (weight loss restores menstrual regularity in many), metformin, combined oral contraceptives for cycle regulation, letrozole/clomiphene for ovulation induction. IVF: careful stimulation protocols (antagonist protocol, low starting doses) to minimize OHSS risk; freeze-all strategy if OHSS risk high. Granulosa cell tumor: surgical staging and oophorectomy."
        },
        "Normal": {
            "meaning": "AMH 1.0–3.5 ng/mL indicates normal ovarian reserve appropriate for age, predicting normal response to gonadotropin stimulation.",
            "causes": "N/A - This is a normal result.",
            "effects": "Adequate follicular pool for age-appropriate fertility.",
            "solution": "AMH does not predict natural pregnancy odds in the short term. Reassuring but fertility is multifactorial. Repeat annually if fertility planning is delayed."
        }
    },

    # ==========================================================================
    # SECTION 10: VITAMIN / NUTRITION TESTS
    # ==========================================================================

    "vitamin_d": {
        "Low": {
            "meaning": "25-OH Vitamin D below 20 ng/mL indicates vitamin D deficiency; 20–30 ng/mL is insufficiency. Deficiency impairs calcium absorption and is associated with bone disease and multiple systemic effects.",
            "causes": "Inadequate sun exposure (indoor lifestyle, high-latitude residence, covering clothing, sunscreen use), dark skin pigmentation (reduced UV vitamin D synthesis), dietary deficiency, malabsorption (Crohn's, celiac, bariatric surgery), obesity (fat-soluble vitamin sequestration), CKD (impaired 1-hydroxylation), liver disease, medications (anticonvulsants, rifampicin), exclusive breastfeeding without supplementation, elderly (reduced skin synthesis).",
            "effects": "Rickets (children — bowing of legs, craniotabes, rachitic rosary, delayed dentition). Osteomalacia (adults — bone pain, proximal muscle weakness, fragility fractures). Osteoporosis (contributes to with calcium deficiency). Increased fracture risk. Secondary hyperparathyroidism. Associations (causality debated): increased risk of autoimmune diseases, cancers, cardiovascular disease, depression, T2DM, respiratory infections (including COVID-19 severity).",
            "solution": "Replace with vitamin D3 (cholecalciferol) — preferred over D2. Deficiency: 50,000 IU/week for 8–12 weeks (oral), then 1,500–2,000 IU/day maintenance. Severe deficiency or malabsorption: higher doses. Monitor 25-OH Vitamin D level after 3 months. Target: 30–50 ng/mL. For CKD: calcitriol (active form, bypasses renal hydroxylation). Recommend adequate sun exposure (15–30 minutes daily, arms and face)."
        },
        "High": {
            "meaning": "25-OH Vitamin D above 100 ng/mL (vitamin D toxicity) causes hypercalcemia; toxicity virtually only occurs with supplemental overdose, not sun exposure.",
            "causes": "Excessive vitamin D supplementation (supplemental doses >10,000 IU/day over prolonged periods), sarcoidosis/granulomatous diseases (unregulated 1-hydroxylation of vitamin D by macrophages causing excess calcitriol), Williams syndrome, idiopathic infantile hypercalcemia.",
            "effects": "Hypercalcemia: nausea, vomiting, weakness, confusion, polyuria, polydipsia, constipation, renal calculi, nephrocalcinosis, soft tissue calcification.",
            "solution": "Stop vitamin D supplementation and restrict dietary calcium. Hydration. Corticosteroids (suppress calcitriol production in granulomatous disease and vitamin D toxicity). Bisphosphonates or calcitonin for severe hypercalcemia. Treat underlying granulomatous disease."
        },
        "Normal": {
            "meaning": "25-OH Vitamin D 30–100 ng/mL indicates adequate vitamin D status for bone health and calcium absorption.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal calcium and phosphate absorption, bone mineralization, immune modulation, and muscle function.",
            "solution": "Maintain 1,000–2,000 IU vitamin D3 daily for adults, especially in low-sun environments. Dietary sources (fatty fish, fortified dairy). Sun exposure (15–30 min daily). Annual testing for at-risk individuals."
        }
    },

    "vitamin_b12": {
        "Low": {
            "meaning": "Serum B12 below 200 pg/mL (148 pmol/L) indicates deficiency — though functional deficiency (elevated methylmalonic acid and homocysteine) may occur at 'low-normal' levels (200–300 pg/mL).",
            "causes": "Dietary deficiency: strict vegetarians/vegans (B12 is only in animal products), elderly with reduced intake. Malabsorption: pernicious anemia (autoimmune anti-intrinsic factor antibodies — most common cause of severe B12 deficiency in developed countries), Crohn's disease, ileal resection (B12 absorbed in terminal ileum), celiac disease, gastrectomy, bariatric surgery, atrophic gastritis, chronic H. pylori infection. Medications: metformin (reduces ileal B12 absorption), proton pump inhibitors (long-term), H2 blockers, colchicine. Fish tapeworm (Diphyllobothrium).",
            "effects": "Macrocytic megaloblastic anemia: fatigue, pallor, glossitis, angular stomatitis. Neurological (unique to B12 deficiency — not folate): subacute combined degeneration of spinal cord (demyelination of dorsal and lateral columns — paresthesias, weakness, ataxia, spasticity, cognitive decline), peripheral neuropathy, optic neuritis. Elevated homocysteine and methylmalonic acid — markers of functional deficiency. Psychiatric manifestations: depression, psychosis ('megaloblastic madness').",
            "solution": "Pernicious anemia/severe malabsorption: cyanocobalamin or hydroxocobalamin IM (1,000 µg daily for 1 week, then weekly for 4 weeks, then monthly lifelong). Dietary deficiency: high-dose oral B12 (1,000–2,000 µg/day) is as effective as IM if intestinal absorption is intact (passive absorption occurs). Sublingual/intranasal B12 available. Neurological deficits may not fully reverse — treat early. Folate should not be given alone without B12 (can mask anemia while neurological damage progresses)."
        },
        "High": {
            "meaning": "Elevated vitamin B12 (above 900 pg/mL) without supplementation may indicate a serious underlying condition requiring investigation.",
            "causes": "Supplementation/B12 injections (most common — benign), liver disease (hepatocyte release of stored B12), myeloproliferative neoplasms (CML, polycythemia vera — excess transcobalamin from granulocytes), solid tumors (breast, colon, stomach, kidney, hepatocellular carcinoma), renal failure, autoimmune hepatitis.",
            "effects": "Elevated B12 itself does not cause symptoms; the underlying condition (malignancy, liver disease) causes the clinical presentation.",
            "solution": "Exclude supplementation/injection as cause first. If unexplained elevated B12: full CBC, LFTs, bone marrow evaluation, CT scan for malignancy. Elevated B12 in liver disease resolves with hepatic treatment."
        },
        "Normal": {
            "meaning": "B12 200–900 pg/mL confirms adequate stores for neurological function, DNA synthesis, and red blood cell production.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal homocysteine and methylmalonic acid levels; intact myelin production and erythropoiesis.",
            "solution": "Vegans: B12 supplementation (at least 25–100 µg/day or 2,500 µg/week) is essential. Elderly: annual B12 testing. Patients on long-term metformin: annual B12 monitoring."
        }
    },

    "ferritin": {
        "Low": {
            "meaning": "Serum ferritin below 12–30 ng/mL (laboratory-dependent; <30 ng/mL has higher sensitivity) is the most specific marker of depleted iron stores — the earliest and most sensitive indicator of iron deficiency.",
            "causes": "Chronic blood loss (menorrhagia — most common in women, GI bleeding — most common in men, hookworm infection in endemic areas), inadequate dietary iron intake (vegetarian diet, infants on cow's milk, toddlers with poor diet), increased demand (pregnancy, growth periods), malabsorption (celiac disease, post-gastrectomy, inflammatory bowel disease, achlorhydria).",
            "effects": "Iron deficiency without anemia: fatigue, reduced exercise capacity, impaired cognitive function, restless leg syndrome, pica (craving for ice/clay/starch), hair loss, impaired immunity. Iron deficiency anemia: all above plus pallor, dyspnea, tachycardia, koilonychia (spoon-shaped nails), angular stomatitis, glossitis, atrophic gastritis, plummer-vinson syndrome (post-cricoid web, dysphagia).",
            "solution": "Identify and treat source of blood loss (colonoscopy/endoscopy for GI bleeding, gynecological evaluation for menorrhagia, stool for occult blood, ova and parasites). Iron replacement: oral ferrous sulfate 325 mg (65 mg elemental iron) TID — best absorbed on empty stomach with vitamin C. Take on alternate days (reduces GI side effects, increases net absorption). IV iron (ferric carboxymaltose, iron sucrose, low-molecular-weight dextran) for: malabsorption, intolerance, advanced CKD, inflammatory bowel disease, pre-surgical optimization. Recheck ferritin after 3 months of therapy; continue for 3 more months after ferritin normalized to replete stores."
        },
        "High": {
            "meaning": "Elevated ferritin (above 300 ng/mL in men, 200 ng/mL in women) may indicate iron overload or is a non-specific acute phase reactant in inflammatory states.",
            "causes": "Iron overload: hereditary hemochromatosis (HFE gene mutations — C282Y, H63D), multiple blood transfusions (thalassemia, sickle cell disease), dietary iron overload. Inflammation (ferritin is an acute phase reactant): infections, inflammatory diseases (rheumatoid arthritis, SLE, adult-onset Still's disease), malignancy. Liver disease (hepatocellular release): viral hepatitis, alcoholic liver disease, NASH, cirrhosis. Hyperferritinemia-cataract syndrome (rare). Macrophage activation syndrome (MAS)/hemophagocytic lymphohistiocytosis (HLH — extremely high ferritin >10,000).",
            "effects": "Hereditary hemochromatosis (if untreated): liver cirrhosis and hepatocellular carcinoma, diabetes (bronze diabetes), cardiomyopathy, hypogonadism, arthritis, skin bronzing. Inflammatory hyperferritinemia: symptoms of underlying disease.",
            "solution": "Distinguish iron overload from inflammatory causes: transferrin saturation >45% with high ferritin suggests iron overload. HFE gene mutation testing. Liver biopsy for staging if hemochromatosis confirmed. Hereditary hemochromatosis treatment: phlebotomy (500 mL weekly until ferritin <50 ng/mL, then maintenance every 2–4 months). Chelation therapy (deferoxamine IV, deferasirox oral) for transfusion-related iron overload. Treat underlying inflammatory disease for reactive hyperferritinemia."
        },
        "Normal": {
            "meaning": "Ferritin 30–300 ng/mL (men), 12–150 ng/mL (women) reflects adequate iron stores for erythropoiesis and cellular function.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal iron availability for hemoglobin synthesis, enzyme function, and mitochondrial respiration.",
            "solution": "Iron-rich diet (red meat, seafood, legumes, fortified cereals). Vitamin C with plant-source iron to enhance absorption. Screen pregnant women, toddlers, and vegetarians annually."
        }
    },

    "tibc": {
        "Low": {
            "meaning": "TIBC below 250 µg/dL indicates decreased transferrin levels — iron stores may be adequate or excessive, or synthesis is impaired.",
            "causes": "Anemia of chronic disease (inflammation reduces transferrin synthesis — negative acute phase reactant), protein malnutrition (reduced synthesis), iron overload (downregulates transferrin), liver disease (reduced hepatic synthesis), nephrotic syndrome (transferrin loss in urine), sickle cell disease.",
            "effects": "Dependent on underlying condition. Low TIBC with high ferritin and transferrin saturation >45% suggests iron overload.",
            "solution": "Interpret TIBC together with serum iron, ferritin, and transferrin saturation. Treat underlying inflammatory disease, liver disease, or iron overload."
        },
        "High": {
            "meaning": "TIBC above 400 µg/dL indicates increased transferrin, reflecting the body's response to iron deficiency — more binding capacity is synthesized to capture scarce iron.",
            "causes": "Iron deficiency anemia (classic finding), iron deficiency without anemia (early stages), pregnancy, oral contraceptive use (estrogen stimulates transferrin synthesis), chronic blood loss.",
            "effects": "High TIBC in the setting of low ferritin and low serum iron confirms iron deficiency.",
            "solution": "Iron replacement therapy as described under Ferritin. Identify and treat source of blood loss or inadequate intake."
        },
        "Normal": {
            "meaning": "TIBC 250–400 µg/dL with normal transferrin saturation (20–50%) indicates normal iron binding capacity and adequate iron stores.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal iron transport to erythropoietic tissue.",
            "solution": "Evaluate TIBC as part of complete iron studies (serum iron + TIBC + ferritin) for comprehensive iron status assessment."
        }
    },

    # ==========================================================================
    # SECTION 11: URINE TESTS
    # ==========================================================================

    "urine_routine_examination": {
        "Low": {
            "meaning": "Normal urine routine examination (no significant abnormalities) is the desired outcome.",
            "causes": "Healthy renal and urinary tract function.",
            "effects": "Normal urinary composition.",
            "solution": "Routine annual health screening. Maintain adequate hydration."
        },
        "High": {
            "meaning": "Abnormal urine routine examination may reveal protein, glucose, blood, casts, nitrites, leukocyte esterase, bilirubin, urobilinogen, or ketones — each pointing to specific pathology.",
            "causes": "Proteinuria: glomerular disease, UTI. Glycosuria: diabetes, renal glycosuria. Hematuria: UTI, stones, malignancy, glomerulonephritis. Nitrites/leukocyte esterase: UTI. Bilirubin: obstructive jaundice. Urobilinogen: liver disease, hemolysis. Ketones: DKA, starvation. Red blood cell casts: glomerulonephritis. White blood cell casts: pyelonephritis. Granular casts: ATN.",
            "effects": "Depends on the specific abnormality: UTI symptoms (dysuria, frequency, urgency, fever in pyelonephritis), edema and hypertension (nephrotic/nephritic syndrome), flank pain/hematuria (stones).",
            "solution": "Each abnormality requires specific follow-up: urine culture and sensitivity for UTI; blood glucose/HbA1c for glycosuria; renal ultrasound/cystoscopy for hematuria; 24-hour urine protein/renal biopsy for proteinuria; nephrology referral for casts. Treat underlying condition."
        },
        "Normal": {
            "meaning": "Normal urine routine: clear yellow, pH 4.5–8.0, specific gravity 1.005–1.030, no protein, no glucose, no blood, no ketones, no nitrites, no leukocyte esterase, no bilirubin.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal renal filtration, concentration, and urinary tract health.",
            "solution": "Adequate hydration (2–3 L/day). Annual urine examination for at-risk populations (diabetics, hypertensives, elderly, pregnant women)."
        }
    },

    "urine_specific_gravity": {
        "Low": {
            "meaning": "Specific gravity below 1.005 indicates dilute urine — the kidney is excreting excess water or has impaired concentrating ability.",
            "causes": "Overhydration/excessive fluid intake, diabetes insipidus (central or nephrogenic — inability to concentrate urine despite dehydration), SIADH paradoxically can cause dilute urine, medications (lithium-induced nephrogenic DI), early CKD.",
            "effects": "Polyuria (large volumes of dilute urine), nocturia, polydipsia in diabetes insipidus.",
            "solution": "Water deprivation test to diagnose diabetes insipidus. DDAVP stimulation test to distinguish central from nephrogenic DI. DDAVP for central DI. Thiazide diuretics + low-solute diet for nephrogenic DI. Stop lithium if causing nephrogenic DI."
        },
        "High": {
            "meaning": "Specific gravity above 1.030 indicates concentrated urine — the kidney is conserving water, consistent with dehydration or high ADH state.",
            "causes": "Dehydration, SIADH, heart failure, cirrhosis, hypovolemia, excessive sweating, poor fluid intake.",
            "effects": "Concentrated dark urine, oliguria, thirst. Prolonged dehydration: prerenal azotemia, increased renal stone risk.",
            "solution": "Increase fluid intake. Treat underlying cause of dehydration. Monitor urine output and renal function if dehydration is significant."
        },
        "Normal": {
            "meaning": "Specific gravity 1.005–1.030 reflects normal renal concentrating and diluting ability in response to hydration status.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal water balance and renal tubular function.",
            "solution": "Maintain adequate hydration. SG is higher in concentrated morning urine — use spot AM specimen for routine urinalysis."
        }
    },

    "urine_ph": {
        "Low": {
            "meaning": "Urine pH below 5.0 is highly acidic, reflecting metabolic acidosis or high acid load.",
            "causes": "High-protein/low-carbohydrate diet, metabolic acidosis (DKA, lactic acidosis), respiratory alkalosis compensation, uric acid nephrolithiasis (acidic urine precipitates urate crystals), gout, severe diarrhea.",
            "effects": "Very acidic urine predisposes to uric acid stone formation. Generally reflects acid-base status.",
            "solution": "Alkalinize urine (potassium citrate, sodium bicarbonate) for recurrent uric acid stones. Treat underlying metabolic acidosis."
        },
        "High": {
            "meaning": "Urine pH above 7.5 is alkaline, indicating high bicarbonate excretion or UTI with urease-producing organisms.",
            "causes": "Metabolic alkalosis (vomiting, diuretic use), vegetarian diet (plant-based diet increases bicarbonate), renal tubular acidosis types 1 and 2, UTI with urease-producing bacteria (Proteus, Klebsiella, Pseudomonas — split urea into ammonia → alkaline urine), medication (acetazolamide, antacids).",
            "effects": "Alkaline pH predisposes to calcium phosphate and struvite (magnesium ammonium phosphate) stone formation. UTI with alkaline urine suggests urease-producing organism; struvite stones (staghorn calculi) risk.",
            "solution": "UTI with alkaline pH: culture and treat with appropriate antibiotic targeting urease-producing organism. Acidify urine for recurrent calcium phosphate stones. Correct underlying alkalosis."
        },
        "Normal": {
            "meaning": "Urine pH 5.0–7.0 reflects normal renal acid handling and dietary acid load.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal acid-base regulation through renal hydrogen ion excretion.",
            "solution": "Balanced diet. Adequate hydration. Urine pH used to guide stone prevention strategies and UTI characterization."
        }
    },

    # ==========================================================================
    # SECTION 12: SEROLOGY / INFECTIOUS DISEASE
    # ==========================================================================

    "hbsag": {
        "Low": {
            "meaning": "HBsAg negative indicates absence of hepatitis B surface antigen — the patient is not currently infected with hepatitis B virus.",
            "causes": "Never infected, naturally cleared infection (acute HBV), vaccinated (check anti-HBs), or resolved infection (anti-HBc positive, HBsAg negative).",
            "effects": "Not currently infectious. Immune if anti-HBs positive (>10 mIU/mL).",
            "solution": "If unvaccinated: recommend hepatitis B vaccine series (3 doses). If vaccinated: confirm immunity with anti-HBs. Screen high-risk groups annually."
        },
        "High": {
            "meaning": "HBsAg positive for >6 months indicates chronic hepatitis B infection; acute infection may be HBsAg positive for <6 months. HBsAg positivity means the patient is infectious.",
            "causes": "Transmission via: blood/body fluids (IV drug use, unprotected sex, healthcare exposure), mother-to-child at birth (most common route in endemic areas — Asia, sub-Saharan Africa).",
            "effects": "Acute HBV: jaundice, fatigue, RUQ pain, elevated LFTs, spontaneous resolution in 95% of adults. Chronic HBV: cirrhosis (20–25% of chronic carriers), hepatocellular carcinoma (HCC — 15–25-fold increased risk), liver failure. Vertical transmission leads to immune-tolerant chronic infection in 90% of infected neonates.",
            "solution": "Confirm chronic status (>6 months). Assess disease activity: HBeAg/anti-HBe, HBV DNA viral load, ALT, liver fibrosis staging (biopsy or FibroScan). Antiviral therapy indication: HBV DNA >2,000 IU/mL + elevated ALT or significant fibrosis: tenofovir alafenamide (TAF) or entecavir (first-line — both with high barrier to resistance). HCC surveillance: 6-monthly liver ultrasound + AFP. Vaccinate all household contacts. Newborn of HBsAg+ mother: HBIG + vaccine within 12 hours of birth."
        },
        "Normal": {
            "meaning": "HBsAg negative — no evidence of active hepatitis B infection.",
            "causes": "N/A - This is a normal result.",
            "effects": "Not infected with or actively shedding hepatitis B virus.",
            "solution": "Vaccination if not immune. Screen for hepatitis B in high-risk populations: healthcare workers, IV drug users, sexual partners of HBsAg+ individuals, travelers to endemic areas, immigrants from endemic regions."
        }
    },

    "anti_hcv": {
        "Low": {
            "meaning": "Anti-HCV negative indicates no antibody response to hepatitis C virus — consistent with never having been infected (or very early acute infection before antibody development — window period 8–12 weeks).",
            "causes": "No HCV exposure, or very early acute HCV infection (PCR-positive but seronegative during window period), severe immunosuppression (may not mount antibody response — check HCV RNA in immunocompromised patients).",
            "effects": "Not currently infected with or exposed to hepatitis C (with caveats above).",
            "solution": "Screen high-risk individuals: IV drug users, HIV-positive, received blood transfusion before 1992, hemodialysis patients, healthcare workers with needlestick exposure, children born to HCV-positive mothers. One-time universal screening recommended for all adults born 1945–1965 (birth cohort screening)."
        },
        "High": {
            "meaning": "Anti-HCV positive indicates exposure to hepatitis C virus. Unlike hepatitis B, anti-HCV does not confer immunity and a positive result requires confirmation with HCV RNA to determine active infection.",
            "causes": "IV drug use (sharing needles — most common in developed countries), unscreened blood transfusion (pre-1992), hemodialysis, sexual transmission (low risk), tattooing/piercing with unsterilized equipment, mother-to-child transmission, healthcare occupational exposure.",
            "effects": "Acute HCV: 80% asymptomatic; 20% mild jaundice. Spontaneous clearance in only 15–25%. Chronic HCV (75–85%): silent progression over 20–30 years to cirrhosis (20%), HCC (5%), liver failure. HCV is now the leading indication for liver transplantation in many countries. Extrahepatic: cryoglobulinemia, membranoproliferative glomerulonephritis, non-Hodgkin lymphoma, porphyria cutanea tarda.",
            "solution": "Confirm active infection with HCV RNA (quantitative). If HCV RNA positive: genotype (1–6 — guides treatment regimen). Direct-acting antiviral (DAA) therapy: pan-genotypic — sofosbuvir/velpatasvir (Epclusa) or glecaprevir/pibrentasvir (Mavyret) — 8–12 week courses achieve >95% sustained virological response (SVR — cure). SVR reduces HCC risk by 70%, reduces all-cause mortality. No HCV vaccine available — harm reduction strategies (needle exchange programs, opioid substitution therapy, condom use)."
        },
        "Normal": {
            "meaning": "Anti-HCV negative indicates no detectable HCV antibody — consistent with absence of prior infection.",
            "causes": "N/A - This is a normal result.",
            "effects": "No hepatitis C viral exposure detected.",
            "solution": "Risk reduction: sterile needle use, avoid sharing personal hygiene items. Universal screening recommended in many countries for all adults at least once."
        }
    },

    "hiv": {
        "Low": {
            "meaning": "Non-reactive HIV test (4th generation Ag/Ab combination test) indicates absence of HIV antigen (p24) and HIV antibodies — consistent with not being infected with HIV.",
            "causes": "No HIV exposure, or within the window period of early infection (p24 Ag appears 10–14 days post-infection, Ab 3–12 weeks). A reactive test must be confirmed by a supplemental differentiation assay.",
            "effects": "No HIV infection (with window period caveat). If recent high-risk exposure, retest at 45 days and 90 days.",
            "solution": "High-risk exposure (<72 hours): HIV post-exposure prophylaxis (PEP) — tenofovir/emtricitabine + raltegravir or dolutegravir for 28 days. For ongoing high risk: HIV pre-exposure prophylaxis (PrEP) — daily tenofovir/emtricitabine (Truvada/Descovy). Condom use, sterile needles, harm reduction."
        },
        "High": {
            "meaning": "Reactive HIV test must be confirmed with a supplemental test (HIV-1/HIV-2 antibody differentiation assay, HIV RNA quantification). Confirmed positive HIV status requires comprehensive evaluation and linkage to care.",
            "causes": "HIV-1 (most common worldwide) or HIV-2 (West Africa primarily) infection via: unprotected sexual contact, sharing injection equipment, blood transfusion, mother-to-child transmission (pregnancy, delivery, breastfeeding).",
            "effects": "Acute HIV infection: flu-like illness (fever, lymphadenopathy, sore throat, rash, myalgia) — 2–4 weeks post-infection. Chronic HIV: CD4 decline over years if untreated. AIDS (CD4 <200/µL): AIDS-defining opportunistic infections (PCP, CMV retinitis, toxoplasma encephalitis, Cryptococcal meningitis, MAC, KS, NHL). HIV-associated non-AIDS conditions: cardiovascular disease, renal disease, neurocognitive impairment, non-AIDS malignancies.",
            "solution": "Confirm diagnosis. CD4 count and HIV viral load. Antiretroviral therapy (ART): initiate immediately for all HIV-positive individuals regardless of CD4 count (universal treatment). Preferred regimens: integrase strand transfer inhibitor (INSTI)-based: bictegravir/tenofovir AF/emtricitabine (Biktarvy) or dolutegravir + tenofovir/emtricitabine. Goal: undetectable viral load (<50 copies/mL), which also means Undetectable = Untransmittable (U=U). OI prophylaxis (CD4 <200: PCP prophylaxis with TMP-SMX; CD4 <50: MAC prophylaxis). Routine monitoring: CD4, viral load, CBC, metabolic panel, STI screening."
        },
        "Normal": {
            "meaning": "Non-reactive HIV test — no detectable HIV antigen or antibodies.",
            "causes": "N/A - This is a normal result.",
            "effects": "No HIV infection at the time of testing (with window period caveat).",
            "solution": "HIV prevention: consistent condom use, PrEP for high-risk individuals, harm reduction for PWID, HIV testing at least annually for sexually active adults with multiple partners. Know your HIV status — routine opt-out testing recommended by WHO."
        }
    },

    "dengue_ns1": {
        "Low": {
            "meaning": "Dengue NS1 antigen negative makes acute dengue infection unlikely in the first 5 days of fever but does not fully exclude dengue.",
            "causes": "No dengue infection, or NS1 may become negative after day 5–6 of illness (clearance of viremia).",
            "effects": "Dengue is less likely; consider alternative febrile illness diagnoses.",
            "solution": "If dengue still clinically suspected beyond day 5: check dengue IgM antibody. Consider malaria blood film and leptospira testing for differential diagnosis in endemic settings."
        },
        "High": {
            "meaning": "Positive dengue NS1 antigen (nonstructural protein 1) confirms current dengue virus infection, particularly in the febrile phase (days 1–5 of illness).",
            "causes": "Dengue virus (serotypes DENV 1–4) transmitted by Aedes aegypti and Aedes albopictus mosquito bites in tropical/subtropical regions (South/Southeast Asia, Caribbean, Latin America, sub-Saharan Africa).",
            "effects": "Febrile phase (days 1–3): high fever, headache, retroorbital pain, myalgia, arthralgia ('breakbone fever'), nausea. Critical phase (days 4–6): defervescence with risk of plasma leakage (pleural effusion, ascites), dengue hemorrhagic fever (DHF), dengue shock syndrome (DSS). Recovery phase (days 7–10): reabsorption of fluids, bradycardia, rash. Warning signs indicating severe dengue: abdominal pain, persistent vomiting, bleeding gums, lethargy, restlessness, rapid breathing, rising hematocrit with falling platelet count.",
            "solution": "Supportive management — no specific antiviral. Paracetamol (acetaminophen) for fever/pain — strictly AVOID NSAIDs and aspirin (bleeding risk with low platelets). Oral rehydration with ORS for uncomplicated dengue. IV isotonic crystalloid if oral intake poor or warning signs present. Monitor daily CBC (platelet count and hematocrit). Hospitalize for DHF/DSS: careful IV fluid titration (avoid overhydration — risk of fluid overload in recovery phase), platelet transfusion only if <10,000/µL or active significant bleeding. No prophylactic platelet transfusion."
        },
        "Normal": {
            "meaning": "NS1 antigen negative: no evidence of acute dengue viremia.",
            "causes": "N/A - This is a normal result.",
            "effects": "Current dengue infection effectively ruled out in febrile phase (days 1–5).",
            "solution": "Dengue prevention: eliminate Aedes mosquito breeding sites (stagnant water), use mosquito repellents (DEET), protective clothing, bed nets. Dengvaxia vaccine available in some countries for seropositive individuals only."
        }
    },

    "widal_test": {
        "Low": {
            "meaning": "Widal test negative (O and H agglutinin titers <1:80) suggests absence of current Salmonella typhi infection or recent vaccination with typhoid vaccine.",
            "causes": "No typhoid fever, or very early infection before antibody development, or patient has not mounted an adequate antibody response (immunosuppressed).",
            "effects": "Typhoid is unlikely if negative in appropriate clinical and epidemiological context.",
            "solution": "If clinical suspicion persists: blood culture (gold standard for typhoid diagnosis), bone marrow culture (most sensitive), stool culture. Widal test has limited specificity — should not be used in isolation."
        },
        "High": {
            "meaning": "Widal test positive (O antigen titer ≥1:160 or H antigen titer ≥1:160, or rising titer in paired samples) suggests current or recent typhoid fever. Widal test is neither sensitive nor specific — blood culture remains the gold standard.",
            "causes": "Salmonella typhi (typhoid fever), Salmonella paratyphi A, B, C (enteric fever). Transmission: fecal-oral route through contaminated food and water in endemic regions (South Asia, sub-Saharan Africa, Southeast Asia).",
            "effects": "Stepwise fever (rising over days), headache, relative bradycardia, rose spots (trunk rash — rare), splenomegaly, abdominal tenderness, constipation or diarrhea. Complications: intestinal perforation (serious — peritonitis), hemorrhage, encephalopathy, hepatitis, myocarditis.",
            "solution": "Blood culture first. Antibiotics: azithromycin (oral — for uncomplicated typhoid, reduced resistance), ceftriaxone IV (for severe typhoid or fluoroquinolone-resistant strains), fluoroquinolones (ciprofloxacin — high resistance in South Asia, not first-line). Dexamethasone for severe typhoid with altered consciousness. Supportive care: oral rehydration. Typhoid vaccine (Vi polysaccharide or Ty21a oral) for travelers. Clean water and sanitation for prevention."
        },
        "Normal": {
            "meaning": "Widal titers within normal/low range indicate no significant current typhoid fever antibody response.",
            "causes": "N/A - This is a normal result.",
            "effects": "No significant agglutinating antibody response to Salmonella typhi antigens.",
            "solution": "Gold standard for typhoid diagnosis is blood culture. Use Widal test judiciously — endemic area baseline titers may be falsely elevated. Typhoid vaccination and food/water hygiene for prevention."
        }
    },

    "malaria_parasite": {
        "Low": {
            "meaning": "Negative malaria parasite (MP) smear or negative rapid diagnostic test (RDT) indicates absence of malaria parasites in the peripheral blood at the time of testing.",
            "causes": "No malaria infection, parasitemia below detection threshold (early infection, low-density parasitemia), partial immunity, or recent partial treatment.",
            "effects": "Malaria is unlikely if both thick and thin smear are negative and clinical suspicion is low.",
            "solution": "If clinical suspicion remains high (endemic area exposure, characteristic fever pattern): repeat smear every 12–24 hours for 72 hours. PCR malaria if available (more sensitive for low-density parasitemia). Consider alternative diagnosis (dengue, typhoid, leptospirosis)."
        },
        "High": {
            "meaning": "Positive malaria parasite smear or RDT confirms malaria infection. Species identification (Plasmodium falciparum, vivax, malariae, ovale, knowlesi) is critical for management.",
            "causes": "Plasmodium species transmitted by female Anopheles mosquito bites in endemic regions (sub-Saharan Africa, South Asia, Southeast Asia, Central/South America, Pacific Islands).",
            "effects": "Uncomplicated malaria: cyclical fever (tertian — 48h cycle for P. vivax/ovale, quartan — 72h for P. malariae), rigors, headache, myalgia, sweating, nausea. Severe malaria (predominantly P. falciparum): cerebral malaria (coma, seizures), severe anemia, respiratory distress, hypoglycemia, acute kidney injury, circulatory collapse, blackwater fever (massive hemolysis with hemoglobinuria). P. vivax/ovale: relapse from dormant liver hypnozoites.",
            "solution": "P. falciparum (uncomplicated): artemisinin-based combination therapy (ACT) — artemether/lumefantrine or artesunate/amodiaquine. Severe P. falciparum: IV artesunate (superior to quinine — reduces mortality). P. vivax/ovale: chloroquine (or ACT in chloroquine-resistant areas) + primaquine for radical cure (eliminate hypnozoites — check G6PD status before primaquine). Prevention: insecticide-treated bed nets, indoor residual spraying, chemoprophylaxis for travelers, RTS,S/AS01 malaria vaccine (children in sub-Saharan Africa)."
        },
        "Normal": {
            "meaning": "No malaria parasites detected on peripheral blood smear or by rapid antigen testing.",
            "causes": "N/A - This is a normal result.",
            "effects": "No current malaria infection.",
            "solution": "Malaria prevention when traveling to endemic areas: chemoprophylaxis (atovaquone/proguanil, doxycycline, or mefloquine based on destination resistance patterns), DEET-based repellents, permethrin-treated clothing, bed nets."
        }
    },

    "mantoux_test": {
        "Low": {
            "meaning": "Negative Mantoux (TST <5 mm induration, or <10 mm in high-risk groups) indicates no prior exposure to Mycobacterium tuberculosis or BCG vaccine response has waned. May be falsely negative (anergy) in immunosuppressed states.",
            "causes": "No prior TB exposure, BCG vaccine distant in time, immunosuppression (HIV, severe malnutrition, high-dose steroids — anergy), very early TB infection (before immune response), incorrect technique, elderly with waned response.",
            "effects": "Effective rule-out of latent TB infection in immunocompetent individuals with low pre-test probability.",
            "solution": "Consider TB-IGRA (interferon-gamma release assay — QuantiFERON-TB Gold, T-SPOT.TB) as alternative or supplementary test — not affected by BCG vaccination or NTM. Repeat TST if initial reaction borderline or anergy suspected."
        },
        "High": {
            "meaning": "Positive Mantoux (TST ≥10 mm induration in general population, ≥5 mm in HIV-positive or immunosuppressed, ≥15 mm in low-risk adults) indicates prior exposure to Mycobacterium tuberculosis (latent TB infection) or BCG vaccination effect.",
            "causes": "Latent TB infection (LTBI — most important cause), BCG vaccination (weaker reaction, usually <15 mm), prior active TB (treated or untreated), exposure to non-tuberculous mycobacteria (weaker cross-reaction).",
            "effects": "Positive TST alone ≠ active TB. LTBI carries 5–10% lifetime risk of progression to active TB; risk increases dramatically with immunosuppression, malnutrition, and certain medications (anti-TNF therapy).",
            "solution": "Active TB must be excluded (chest X-ray, sputum smear/culture/GeneXpert). If active TB excluded: treat LTBI — isoniazid (INH) 300 mg daily for 6–9 months, or rifampicin for 4 months, or 3 months of weekly INH + rifapentine (3HP) — all effective in preventing progression. Prioritize LTBI treatment for HIV-positive, recent converters, anti-TNF therapy candidates, immunosuppressed patients. Pyridoxine (vitamin B6) with INH to prevent peripheral neuropathy."
        },
        "Normal": {
            "meaning": "Negative Mantoux test indicates no detectable delayed hypersensitivity to tuberculin antigen.",
            "causes": "N/A - This is a normal result.",
            "effects": "No prior TB exposure or immune response to Mycobacterium tuberculosis.",
            "solution": "Annual TST screening for high-risk individuals (healthcare workers, TB contacts, HIV-positive, immunosuppressed). Consider TB-IGRA for individuals with prior BCG vaccination."
        }
    },    # ==========================================================================
    # SECTION 13: AUTOIMMUNE / IMMUNOLOGY TESTS
    # ==========================================================================

    "ana": {
        "Low": {
            "meaning": "ANA negative (titer <1:40 or below laboratory threshold) makes systemic lupus erythematosus (SLE) very unlikely — sensitivity of ANA for SLE is >95%.",
            "causes": "No autoimmune condition, low titer (borderline) in healthy individuals (5–15% of normal population can have low-titer ANA without disease).",
            "effects": "SLE is effectively ruled out in most cases. Other ANA-negative autoimmune conditions exist (ANA-negative lupus — rare, seronegative inflammatory arthritis).",
            "solution": "Negative ANA is very reassuring against SLE. Consider myositis-specific antibodies (anti-Jo-1, anti-Mi-2) for myositis, anti-CCP/RF for RA in seronegative context. Continue clinical evaluation based on symptoms."
        },
        "High": {
            "meaning": "Positive ANA (titer ≥1:80, or >1:160 is more significant) indicates autoimmune nuclear protein antibodies. ANA is a screening test — must be followed by specific antibody testing (anti-dsDNA, ENA panel) to characterize the underlying autoimmune condition.",
            "causes": "SLE (anti-dsDNA, anti-Sm most specific), systemic sclerosis/scleroderma (anti-Scl-70, anti-centromere), Sjögren's syndrome (anti-Ro/SSA, anti-La/SSB), mixed connective tissue disease (anti-U1RNP), polymyositis/dermatomyositis (anti-Jo-1), drug-induced lupus (anti-histone), juvenile idiopathic arthritis, rheumatoid arthritis. Low-titer ANA: healthy individuals, first-degree relatives of lupus patients, elderly, infections (EBV, HIV), malignancy, certain medications (hydralazine, procainamide, isoniazid, minocycline).",
            "effects": "Varies with underlying disease: SLE — multisystem disease (nephritis, serositis, arthritis, cytopenias, CNS involvement, malar rash, photosensitivity); scleroderma — skin fibrosis, Raynaud's, ILD, PAH; Sjögren's — dry eyes/mouth, fatigue.",
            "solution": "Follow positive ANA with anti-dsDNA, anti-Sm, anti-Ro/SSA, anti-La/SSB, anti-Scl-70, anti-centromere, anti-U1RNP, anti-histone. Refer to rheumatologist. Determine if clinical criteria for specific autoimmune disease are met (SLICC criteria for SLE). Hydroxychloroquine for SLE (baseline therapy — reduces flares and organ damage). Disease-specific treatment for each condition."
        },
        "Normal": {
            "meaning": "ANA negative indicates no significant antinuclear antibodies detected.",
            "causes": "N/A - This is a normal result.",
            "effects": "SLE and most connective tissue diseases are effectively excluded.",
            "solution": "If symptoms suggestive of autoimmune disease persist despite negative ANA: consider anti-Ro, anti-Jo-1 (anti-synthetase syndrome), ANCA (vasculitis), myositis-specific antibodies. Rheumatology referral for diagnostic uncertainty."
        }
    },

    "rheumatoid_factor": {
        "Low": {
            "meaning": "Negative RF indicates no detectable rheumatoid factor — most commonly IgM antibodies against the Fc portion of IgG. Seronegative RA is common (20–30% of RA patients).",
            "causes": "No rheumatoid factor production. Early RA (seroconversion may occur months to years into disease).",
            "effects": "Seronegative RA tends to have less severe joint destruction and extra-articular manifestations than seropositive RA.",
            "solution": "Seronegative RA diagnosis is clinical (ACR/EULAR criteria). Anti-CCP is more specific than RF — test both. Continue disease-modifying antirheumatic drug (DMARD) therapy based on clinical assessment."
        },
        "High": {
            "meaning": "Elevated RF is present in 70–80% of RA patients but is not specific — found in many other conditions. High-titer RF combined with positive anti-CCP is highly specific for RA.",
            "causes": "Rheumatoid arthritis (most important), Sjögren's syndrome, SLE, mixed cryoglobulinemia (hepatitis C-associated — very high IgM RF), infective endocarditis, chronic hepatitis B and C, TB, sarcoidosis, healthy elderly (low-titer RF), hypergammaglobulinemia.",
            "effects": "RA: symmetric small joint polyarthritis (MCPs, PIPs, wrists), morning stiffness >1 hour, joint erosions, rheumatoid nodules, extra-articular manifestations (ILD, vasculitis, scleritis, Felty's syndrome, Caplan syndrome).",
            "solution": "Diagnose RA using ACR/EULAR 2010 criteria (score-based). Disease-modifying treatment: methotrexate (first-line DMARD — weekly oral or SC). Add biologic DMARDs (TNF inhibitors: adalimumab, etanercept; IL-6 inhibitors: tocilizumab; JAK inhibitors: baricitinib, tofacitinib) for inadequate response. Low-dose corticosteroids as bridging therapy. Treat to target (DAS28 remission)."
        },
        "Normal": {
            "meaning": "RF negative or within normal titer indicates absence of significant rheumatoid factor.",
            "causes": "N/A - This is a normal result.",
            "effects": "Rheumatoid arthritis is less likely, but seronegative RA is possible.",
            "solution": "Test anti-CCP (more specific than RF) if RA is suspected. Clinical examination and imaging (X-rays, ultrasound) guide diagnosis."
        }
    },

    "crp": {
        "Low": {
            "meaning": "CRP below 5 mg/L indicates absent or minimal acute phase response — no significant acute inflammation or infection.",
            "causes": "Normal health, absence of infection, inflammation, or tissue injury.",
            "effects": "No evidence of significant systemic inflammation.",
            "solution": "No specific investigation needed. CRP can be normal in viral infections, SLE flares (unreliable in SLE), and early infections."
        },
        "High": {
            "meaning": "Elevated CRP reflects acute phase response: mild elevation (5–20 mg/L) — mild inflammation; moderate (20–100 mg/L) — significant infection or inflammation; high (>100 mg/L) — severe bacterial infection, severe inflammatory flare, extensive tissue injury.",
            "causes": "Bacterial infections (marked elevation — often >100 mg/L), inflammatory diseases (RA, inflammatory bowel disease, vasculitis), tissue injury (MI, surgery, trauma), malignancy, autoimmune disease flares (except SLE — CRP often paradoxically low in SLE without serositis), pancreatitis, burns.",
            "effects": "Reflects but does not cause clinical symptoms. High CRP supports bacterial over viral etiology. In RA: correlates with disease activity. Post-MI CRP elevation predicts worse prognosis.",
            "solution": "CRP guides clinical decision-making: in febrile patients, CRP >100 mg/L strongly suggests bacterial infection warranting antibiotics. CRP used to monitor treatment response in infection, RA, and IBD. hs-CRP (high-sensitivity) is used for cardiovascular risk stratification (see below)."
        },
        "Normal": {
            "meaning": "CRP below 5 mg/L confirms absence of significant acute phase reaction.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal hepatic acute-phase protein production without significant inflammatory stimulus.",
            "solution": "Normal CRP in a febrile patient should raise suspicion of viral etiology. Negative CRP does not exclude all infections or inflammatory conditions."
        }
    },

    "hs_crp": {
        "Low": {
            "meaning": "hs-CRP below 1 mg/L indicates low cardiovascular inflammatory risk (<1.0 mg/L = low risk).",
            "causes": "Absence of subclinical vascular inflammation, healthy lifestyle, non-smoker, healthy weight, regular exercise, anti-inflammatory diet (Mediterranean diet).",
            "effects": "Low cardiovascular event risk based on inflammatory marker. hs-CRP is an independent risk marker for MI, stroke, and cardiovascular death.",
            "solution": "Continue heart-healthy lifestyle: Mediterranean diet, regular physical activity (150 min moderate/week), maintain healthy BMI, avoid smoking. hs-CRP can be monitored every 1-2 years if other risk factors present."
        },
        "Moderate": {
            "meaning": "hs-CRP 1.0–3.0 mg/L indicates moderate cardiovascular inflammatory risk.",
            "causes": "Low-grade chronic inflammation — may be due to obesity (adipose tissue inflammation), metabolic syndrome, sedentary lifestyle, poor diet (high in refined carbs, saturated fats), periodontal disease, chronic stress, occult infection.",
            "effects": "Moderate increased risk of future cardiovascular events. hs-CRP >2 mg/L is associated with 2-fold increased risk of MI compared to <1 mg/L.",
            "solution": "Lifestyle modification: weight loss (5-10% body weight reduces hs-CRP by 20-30%), Mediterranean diet (rich in omega-3s: fatty fish, nuts, olive oil), statin therapy if indicated by ASCVD risk score (statins reduce hs-CRP by 20-50%). Consider screening for metabolic syndrome (fasting glucose, lipids, blood pressure)."
        },
        "High": {
            "meaning": "hs-CRP >3.0 mg/L indicates high cardiovascular inflammatory risk (>3.0 mg/L = high risk).",
            "causes": "Active inflammation — obesity (BMI >30), metabolic syndrome, poorly controlled autoimmune disease (RA, IBD, psoriasis), chronic infection, smoking, significant periodontal disease, malignancy, acute infection (should re-test when well).",
            "effects": "High risk of MI, stroke, and cardiovascular mortality. Elevated hs-CRP is a stronger predictor of vascular events than LDL cholesterol in some populations.",
            "solution": "Exclude acute or chronic inflammatory conditions before attributing to cardiovascular risk. If no alternative cause: aggressive risk factor modification. Statin therapy is indicated for primary prevention if 10-year ASCVD risk ≥7.5% and hs-CRP >2 mg/L (JUPITER trial evidence). Aspirin may be considered for primary prevention in high-risk patients (age 50-69 with 10-year CVD risk ≥10% and hs-CRP >2 mg/L). Treat underlying cause if identified."
        },
        "Normal": {
            "meaning": "hs-CRP <1.0 mg/L indicates low cardiovascular inflammatory risk.",
            "causes": "N/A - This is an optimal result.",
            "effects": "favorable cardiovascular risk profile regarding inflammation.",
            "solution": "Maintain healthy lifestyle to preserve low hs-CRP. Repeat testing every 2-5 years depending on other risk factors."
        }
    },

    "esr": {
        "Low": {
            "meaning": "Low ESR (<15 mm/hr for men, <20 mm/hr for women) indicates no significant acute phase response.",
            "causes": "Normal health, polycythemia (increased red cell mass slows sedimentation), sickle cell disease (abnormal RBC shape), hypofibrinogenemia, very high WBC count, very high platelet count.",
            "effects": "No evidence of significant inflammation — useful for excluding temporal arteritis/polymyalgia rheumatica (highly sensitive).",
            "solution": "Low ESR is not clinically significant. However, in suspected temporal arteritis with normal ESR, consider repeating or getting CRP (more sensitive and faster to rise)."
        },
        "High": {
            "meaning": "Elevated ESR indicates presence of acute phase reactants (primarily fibrinogen) — non-specific marker of inflammation, infection, or tissue injury. Marked elevation (>100 mm/hr) strongly suggests serious underlying condition.",
            "causes": "Infection (bacterial, TB — any cause), inflammatory disease (RA, polymyalgia rheumatica, giant cell/temporal arteritis, IBD, vasculitis), tissue necrosis (MI, pancreatitis), malignancy (lymphoma, multiple myeloma — high ESR is common, metastatic cancer), autoimmune disease, pregnancy (physiological elevation), anemia (speeds sedimentation), nephrotic syndrome, hyperfibrinogenemia, elderly (age-related).",
            "effects": "Non-specific marker but useful for monitoring disease activity (RA, polymyalgia rheumatica). Very high ESR (>100 mm/hr) warrants investigation for occult infection, malignancy, or vasculitis.",
            "solution": "ESR is an acute phase reactant. Clinical context is paramount. Very high ESR: evaluate for infection (blood cultures, CXR, urinalysis), inflammatory disease (CRP, ANA, RF, ANCA), monoclonal gammopathy (SPEP/UPEP), malignancy (age-appropriate cancer screening). Treat underlying condition — ESR normalizes with treatment response (lag time weeks to months). Polymyalgia rheumatica/temporal arteritis: rapid response (days) to low-to-moderate dose corticosteroids (prednisone 15-40 mg/day)."
        },
        "Normal": {
            "meaning": "Normal ESR indicates no evidence of significant acute phase reaction at this time — however, normal ESR does NOT exclude serious disease (especially in early stages or certain conditions).",
            "causes": "N/A - This is a normal result, but be aware of false negatives.",
            "effects": "NSAIDs, statins, steroids, and other anti-inflammatory medications lower ESR and may mask underlying disease.",
            "solution": "If clinical suspicion for serious disease is high (e.g., temporal arteritis, vasculitis, malignancy) despite normal ESR, further investigation is warranted (CRP is more sensitive and rises faster)."
        }
    },

    # ==========================================================================
    # SECTION 14: IRON STUDIES
    # ==========================================================================

    "serum_iron": {
        "Low": {
            "meaning": "Low serum iron indicates decreased circulating iron — often seen in iron deficiency anemia, anemia of chronic disease (functional iron deficiency), or recent blood loss.",
            "causes": "Iron deficiency (most common — inadequate dietary intake, malabsorption, chronic blood loss: GI bleeding, menorrhagia), anemia of chronic disease (inflammatory cytokines block iron release from stores), hypothyroidism, malnutrition, pregnancy (increased demand).",
            "effects": "Impaired erythropoiesis (reduced hemoglobin synthesis) if prolonged — microcytic, hypochromic anemia develops. Fatigue, pallor, reduced exercise capacity.",
            "solution": "Interpret with ferritin (gold standard for iron stores). Low serum iron + low ferritin = absolute iron deficiency — treat with oral ferrous sulfate 325 mg (65 mg elemental iron) + vitamin C (enhances absorption) or IV iron if malabsorption/poor tolerance. Low serum iron + normal/high ferritin = anemia of chronic disease — treat underlying inflammatory condition; IV iron may benefit functional iron deficiency."
        },
        "High": {
            "meaning": "High serum iron indicates increased circulating iron — may be due to iron overload, hemochromatosis, hemolytic anemia, or recent iron ingestion (supplements, blood transfusion).",
            "causes": "Hereditary hemochromatosis (HFE gene mutations — C282Y, H63D — most common genetic disorder in Caucasians), iron supplementation (overuse), multiple blood transfusions (transfusional iron overload), hemolytic anemia (released iron from lysed RBCs), ineffective erythropoiesis (thalassemia — iron loading occurs), liver disease (alcoholic liver disease, hepatitis C). Acute hepatitis (release of hepatocellular iron).",
            "effects": "Iron overload leads to organ toxicity: liver (cirrhosis, HCC), heart (cardiomyopathy, arrhythmia), pancreas (diabetes — bronze diabetes), skin (hyperpigmentation — bronze skin), joints (arthropathy), gonads (hypogonadism).",
            "solution": "Confirm iron overload with ferritin and transferrin saturation (TSAT >45% is abnormal). HFE genotyping for suspected hemochromatosis. Phlebotomy (therapeutic — remove 450-500 mL blood weekly until ferritin <50 ng/mL, then maintenance phlebotomy every 2-4 months). Iron chelation (deferasirox, deferoxamine, deferiprone) for transfusion-dependent anemias. Avoid iron supplements, vitamin C (increases iron absorption), and alcohol."
        },
        "Normal": {
            "meaning": "Normal serum iron indicates adequate circulating iron level — but does NOT rule out iron deficiency if chronic disease or recent iron ingestion is present.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal iron transport at this time.",
            "solution": "Interpret with ferritin and TIBC for complete iron status assessment."
        }
    },

    "ferritin": {
        "Low": {
            "meaning": "Low ferritin (<15-30 ng/mL) is diagnostic for absolute iron deficiency — even before anemia develops. Ferritin is the most sensitive and specific test for iron deficiency.",
            "causes": "Chronic blood loss (GI: peptic ulcer, colon cancer, angiodysplasia, hemorrhoids; menstrual: menorrhagia; urinary: hematuria), inadequate dietary intake (vegans, elderly, low socioeconomic status), malabsorption (celiac disease, H. pylori, gastric bypass, atrophic gastritis, chronic PPI use), pregnancy (high demand), blood donation, hookworm in endemic areas.",
            "effects": "Depleted iron stores → impaired erythropoiesis → iron deficiency anemia (hypochromic, microcytic → low MCV, MCH, high RDW). Symptoms: fatigue, pallor, pica (craving ice/dirt), restless legs syndrome, hair loss, koilonychia (spoon nails), angular cheilitis, glossitis.",
            "solution": "Oral iron replacement: ferrous sulfate 325 mg (65 mg elemental iron) three times daily — best absorbed on empty stomach. Take with vitamin C (500 mg) to enhance absorption. Duration: 3-6 months to replenish stores after hemoglobin normalizes. Identify and treat underlying cause (refer for GI evaluation if no obvious cause in older men/postmenopausal women — colonoscopy indicated). IV iron (ferric carboxymaltose, iron sucrose) for intolerance/malabsorption/severe deficiency. Response: hemoglobin rises 1-2 g/dL over 2-4 weeks."
        },
        "High": {
            "meaning": "High ferritin indicates increased iron stores — but ferritin is also an acute phase reactant (elevated in inflammation, infection, liver disease, malignancy, metabolic syndrome). Must distinguish true iron overload from inflammatory elevation.",
            "causes": "Iron overload: Hereditary hemochromatosis (homozygous C282Y), transfusional overload (thalassemia, MDS, sickle cell). Inflammatory: chronic kidney disease (ferritin often 200-800 ng/mL without iron overload), chronic liver disease (NAFLD, alcoholic liver disease, hepatitis C), RA, IBD, malignancy. Other: metabolic syndrome (obesity, diabetes — ferritin correlates with insulin resistance), acute liver injury (hepatocellular necrosis releases ferritin), porphyria cutanea tarda, hemophagocytic lymphohistiocytosis (extremely high ferritin >10,000 ng/mL).",
            "effects": "Iron overload: organ dysfunction (cirrhosis, HCC, cardiomyopathy, diabetes, hypogonadism, arthropathy). Elevated ferritin due to inflammation: reflects disease activity (monitor trends, not absolute cutoff).",
            "solution": "True iron overload: ferritin >300 ng/mL men, >200 ng/mL women + TSAT >45% + HFE genotyping. Phlebotomy (therapeutic). Inflammatory elevation: treat underlying disease; do not phlebotomize (can worsen anemia of chronic disease). Ferritin is a positive acute phase reactant — can be elevated to 500-1000 ng/mL in inflammation without iron overload. If uncertainty: liver MRI (FerriScan) or liver biopsy for quantitative hepatic iron concentration."
        },
        "Normal": {
            "meaning": "Normal ferritin (30-200 ng/mL in women, 30-300 ng/mL in men) indicates adequate iron stores, assuming no acute inflammation is present.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal body iron stores at this time (about 1-3 grams of stored iron).",
            "solution": "No iron supplementation needed. Continue to include iron-rich foods in diet (red meat, fortified cereals, spinach, legumes). If anemia present with normal ferritin, evaluate for anemia of chronic disease, B12/folate deficiency, or other causes."
        }
    },

    "tibc": {
        "Low": {
            "meaning": "Low TIBC indicates decreased iron-binding capacity — typically seen in anemia of chronic disease (inflammation reduces transferrin production) or protein-losing states.",
            "causes": "Anemia of chronic disease (ACD) — most common cause, malnutrition, liver disease (transferrin produced in liver — cirrhosis reduces production), protein-losing enteropathy, nephrotic syndrome (protein loss), hemochromatosis (low TIBC with high iron/ferritin), malignancy.",
            "effects": "Low TIBC + low serum iron + normal/high ferritin = ACD. Impaired iron delivery to bone marrow despite adequate stores (functional iron deficiency).",
            "solution": "Treat underlying inflammatory condition for ACD. If functional iron deficiency (ACD with low TSAT <20%), IV iron may be beneficial to overcome hepcidin block. Do not use oral iron (poor absorption due to hepcidin) unless very mild."
        },
        "High": {
            "meaning": "High TIBC indicates increased iron-binding capacity — body's response to iron deficiency (increased transferrin production to maximize iron capture and transport).",
            "causes": "Iron deficiency (most common — compensatory increase in transferrin synthesis), late pregnancy, oral contraceptive use, acute hepatitis (increased synthesis).",
            "effects": "High TIBC + low serum iron + low ferritin = iron deficiency. Increased capacity to bind iron — low saturation (TSAT <15% is diagnostic for iron deficiency).",
            "solution": "Iron supplementation (oral ferrous sulfate 325 mg daily or split 2-3 times daily). High TIBC normalizes as iron stores replenish. Duration: at least 3 months after hemoglobin normalization to rebuild stores."
        },
        "Normal": {
            "meaning": "Normal TIBC indicates appropriate iron-binding capacity — interpretation depends on serum iron and ferritin.",
            "causes": "N/A - This is a normal result.",
            "effects": "Normal transferrin production — body's iron transport system is functioning.",
            "solution": "Correlate with serum iron and ferritin. Isolated normal TIBC does not rule out iron deficiency if ferritin is low (early iron deficiency)."
        }
    },

    "transferrin_saturation": {
        "Low": {
            "meaning": "Low transferrin saturation (TSAT <15-20%) indicates insufficient iron available for erythropoiesis — either absolute iron deficiency or functional iron deficiency (anemia of chronic disease).",
            "causes": "Iron deficiency (TSAT <15% + low ferritin + high TIBC), anemia of chronic disease (TSAT <20% + normal/high ferritin + low TIBC), combination of iron deficiency + chronic disease (TSAT low, ferritin low-normal, TIBC variable).",
            "effects": "Erythropoiesis is iron-restricted → microcytic hypochromic anemia (low MCV, low MCH). Compromised red blood cell production.",
            "solution": "Absolute iron deficiency: oral or IV iron replacement. Functional iron deficiency (ACD): treat underlying inflammation; IV iron if TSAT <20% and ferritin <500 ng/mL (in CKD, heart failure, inflammatory bowel disease)."
        },
        "High": {
            "meaning": "High transferrin saturation (TSAT >45-50%) indicates excess iron relative to transferrin binding capacity — suggests iron overload.",
            "causes": "Hereditary hemochromatosis (high TSAT often the earliest abnormality — >50% with ferritin normal initially), iron overload from transfusions, massive iron ingestion, ineffective erythropoiesis with iron loading (thalassemia, MDS, sideroblastic anemia), acute liver necrosis (release of hepatocellular iron).",
            "effects": "Iron not bound to transferrin is non-transferrin-bound iron (NTBI) which is highly toxic to organs (promotes oxidative damage).",
            "solution": "Elevated TSAT >45% + ferritin >200 ng/mL women, >300 ng/mL men in the absence of inflammation → test HFE genotyping (C282Y, H63D). Therapeutic phlebotomy for hemochromatosis. Avoid iron supplements and vitamin C. Long-term monitoring of TSAT and ferritin."
        },
        "Normal": {
            "meaning": "Normal transferrin saturation (20-45%) indicates adequate iron delivery to bone marrow — iron availability is appropriate for erythropoiesis.",
            "causes": "N/A - This is a normal result.",
            "effects": "Iron supply is sufficient for hemoglobin synthesis at this time.",
            "solution": "Normal TSAT does not guarantee normal iron stores — check ferritin for stored iron assessment. Low ferritin with normal TSAT indicates early iron depletion without functional effect yet."
        }
    }
}

# ==========================================================================
# HELPER FUNCTIONS
# ==========================================================================

import re
from typing import Optional, Dict, Any, List, Tuple

# ==========================================================================
# ALIAS MAPPING FUNCTION
# ==========================================================================

from typing import Optional

def normalize_test_name(raw_test_name: Optional[str]) -> Optional[str]:
    """Convert any test name alias to its standard canonical name."""
    if not raw_test_name:  # This handles None, empty string, etc.
        return None
    
    # Rest of your code...
    normalized = raw_test_name.lower().strip()
    # ...
    
    # Normalize input
    normalized = raw_test_name.lower().strip()
    
    # Remove extra spaces, punctuation, and special characters
    normalized = re.sub(r'[^\w\s]', ' ', normalized)
    normalized = re.sub(r'\s+', ' ', normalized)
    normalized = normalized.strip()
    
    # ========== COMPLETE ALIAS DICTIONARY ==========
    aliases = {
        # ===== Hematology =====
        'cbc': 'cbc', 'complete blood count': 'cbc', 'full blood count': 'cbc', 'fbc': 'cbc', 'hemogram': 'cbc',
        'hemoglobin': 'hemoglobin', 'hb': 'hemoglobin', 'hgb': 'hemoglobin', 'haemoglobin': 'hemoglobin',
        'hematocrit': 'hematocrit', 'hct': 'hematocrit', 'pcv': 'hematocrit', 'packed cell volume': 'hematocrit',
        'rbc': 'rbc_count', 'red blood cells': 'rbc_count', 'red blood cell count': 'rbc_count',
        'wbc': 'wbc_count', 'white blood cells': 'wbc_count', 'white blood cell count': 'wbc_count',
        'platelets': 'platelet_count', 'plt': 'platelet_count', 'platelet count': 'platelet_count',
        'esr': 'esr', 'sed rate': 'esr', 'sedimentation rate': 'esr', 'erythrocyte sedimentation rate': 'esr',
        'mcv': 'mcv', 'mean corpuscular volume': 'mcv',
        'mch': 'mch', 'mean corpuscular hemoglobin': 'mch',
        'mchc': 'mchc', 'mean corpuscular hemoglobin concentration': 'mchc',
        'rdw': 'rdw', 'red cell distribution width': 'rdw',
        'peripheral smear': 'peripheral_blood_smear', 'pbs': 'peripheral_blood_smear',
        'reticulocyte': 'reticulocyte_count', 'retic count': 'reticulocyte_count',
        'aec': 'absolute_eosinophil_count', 'eosinophil count': 'absolute_eosinophil_count',
        'dlc': 'dlc', 'differential count': 'dlc', 'differential leukocyte count': 'dlc',
        'tlc': 'tlc', 'total leukocyte count': 'tlc',
        'sickling test': 'sickling_test', 'sickle cell test': 'sickling_test',
        'osmotic fragility': 'osmotic_fragility_test',
        'g6pd': 'g6pd_assay', 'g6pd deficiency': 'g6pd_assay',
        'coombs test': 'coombs_test', 'direct coombs': 'coombs_test', 'direct antiglobulin test': 'coombs_test',
        'hemoglobin electrophoresis': 'hemoglobin_electrophoresis', 'hb electrophoresis': 'hemoglobin_electrophoresis',
        
        # ===== Coagulation =====
        'pt': 'pt', 'prothrombin time': 'pt',
        'inr': 'inr', 'international normalized ratio': 'inr',
        'aptt': 'aptt', 'ptt': 'aptt', 'partial thromboplastin time': 'aptt',
        'bleeding time': 'bleeding_time', 'bt': 'bleeding_time',
        'clotting time': 'clotting_time', 'ct': 'clotting_time',
        'd-dimer': 'd_dimer', 'ddimer': 'd_dimer',
        'fibrinogen': 'fibrinogen',
        'fdp': 'fdp', 'fibrin degradation products': 'fdp',
        'thrombin time': 'thrombin_time', 'tt': 'thrombin_time',
        'factor assay': 'factor_assays', 'factor levels': 'factor_assays',
        
        # ===== Blood Sugar / Diabetes =====
        'fbs': 'fasting_blood_sugar', 'fasting sugar': 'fasting_blood_sugar', 'fasting blood sugar': 'fasting_blood_sugar',
        'rbs': 'random_blood_sugar', 'random sugar': 'random_blood_sugar', 'random blood sugar': 'random_blood_sugar',
        'ppbs': 'ppbs', 'postprandial': 'ppbs', 'postprandial blood sugar': 'ppbs',
        'hba1c': 'hba1c', 'a1c': 'hba1c', 'glycated hemoglobin': 'hba1c',
        'ogtt': 'ogtt', 'glucose tolerance test': 'ogtt',
        'insulin': 'insulin_level', 'serum insulin': 'insulin_level',
        'c-peptide': 'c_peptide', 'c peptide': 'c_peptide',
        'urine sugar': 'urine_sugar', 'urine glucose': 'urine_sugar',
        'urine ketones': 'urine_ketones',
        'fructosamine': 'fructosamine',
        
        # ===== Kidney Function =====
        'blood urea': 'blood_urea', 'urea': 'blood_urea', 'serum urea': 'blood_urea',
        'bun': 'bun', 'blood urea nitrogen': 'bun',
        'creatinine': 'serum_creatinine', 'serum creatinine': 'serum_creatinine', 'creat': 'serum_creatinine',
        'uric acid': 'uric_acid', 'urate': 'uric_acid',
        'egfr': 'egfr', 'estimated gfr': 'egfr', 'gfr': 'egfr',
        'sodium': 'sodium', 'na': 'sodium',
        'potassium': 'potassium', 'k': 'potassium',
        'chloride': 'chloride', 'cl': 'chloride',
        'bicarbonate': 'bicarbonate', 'hco3': 'bicarbonate', 'co2': 'bicarbonate',
        'calcium': 'calcium', 'ca': 'calcium',
        'phosphorus': 'phosphorus', 'phosphate': 'phosphorus',
        'magnesium': 'magnesium', 'mg': 'magnesium',
        'urine protein': 'urine_protein',
        'microalbumin': 'microalbuminuria', 'microalbuminuria': 'microalbuminuria', 'acr': 'microalbuminuria',
        
        # ===== Liver Function =====
        'bilirubin': 'total_bilirubin', 'total bilirubin': 'total_bilirubin', 'tbil': 'total_bilirubin',
        'direct bilirubin': 'direct_bilirubin', 'conjugated bilirubin': 'direct_bilirubin',
        'indirect bilirubin': 'indirect_bilirubin', 'unconjugated bilirubin': 'indirect_bilirubin',
        'alt': 'alt_sgpt', 'sgpt': 'alt_sgpt', 'alanine transaminase': 'alt_sgpt', 'alanine aminotransferase': 'alt_sgpt',
        'ast': 'ast_sgot', 'sgot': 'ast_sgot', 'aspartate transaminase': 'ast_sgot',
        'alp': 'alp', 'alkaline phosphatase': 'alp',
        'ggt': 'ggt', 'gamma gt': 'ggt', 'gamma glutamyl transferase': 'ggt',
        'ldh': 'ldh', 'lactic dehydrogenase': 'ldh',
        'total protein': 'total_protein', 'tp': 'total_protein',
        'albumin': 'albumin', 'alb': 'albumin',
        'globulin': 'globulin',
        'ag ratio': 'ag_ratio', 'a/g ratio': 'ag_ratio', 'albumin globulin ratio': 'ag_ratio',
        'ammonia': 'serum_ammonia', 'serum ammonia': 'serum_ammonia',
        
        # ===== Lipid Profile =====
        'cholesterol': 'total_cholesterol', 'total cholesterol': 'total_cholesterol',
        'hdl': 'hdl_cholesterol', 'hdl cholesterol': 'hdl_cholesterol', 'good cholesterol': 'hdl_cholesterol',
        'ldl': 'ldl_cholesterol', 'ldl cholesterol': 'ldl_cholesterol', 'bad cholesterol': 'ldl_cholesterol',
        'vldl': 'vldl', 'vldl cholesterol': 'vldl',
        'triglycerides': 'triglycerides', 'tg': 'triglycerides',
        
        # ===== Cardiac Markers =====
        'troponin i': 'troponin_i', 'trop i': 'troponin_i',
        'troponin t': 'troponin_t', 'trop t': 'troponin_t',
        'ck-mb': 'ck_mb', 'ckmb': 'ck_mb', 'creatine kinase mb': 'ck_mb',
        'cpk': 'cpk', 'creatine phosphokinase': 'cpk',
        'bnp': 'bnp', 'b-type natriuretic peptide': 'bnp', 'brain natriuretic peptide': 'bnp',
        'nt-probnp': 'nt_probnp',
        'myoglobin': 'myoglobin',
        'homocysteine': 'homocysteine',
        
        # ===== Thyroid Function =====
        'tsh': 'tsh', 'thyroid stimulating hormone': 'tsh',
        't3': 't3', 'triiodothyronine': 't3',
        't4': 't4', 'thyroxine': 't4',
        'free t3': 'free_t3', 'ft3': 'free_t3',
        'free t4': 'free_t4', 'ft4': 'free_t4',
        'anti tpo': 'anti_tpo', 'antithyroid peroxidase': 'anti_tpo', 'tpo antibody': 'anti_tpo',
        'thyroglobulin': 'thyroglobulin',
        
        # ===== Hormonal / Endocrine =====
        'testosterone': 'testosterone', 'total testosterone': 'testosterone',
        'free testosterone': 'free_testosterone',
        'estrogen': 'estrogen', 'estradiol': 'estrogen',
        'progesterone': 'progesterone',
        'lh': 'lh', 'luteinizing hormone': 'lh',
        'fsh': 'fsh', 'follicle stimulating hormone': 'fsh',
        'prolactin': 'prolactin',
        'cortisol': 'cortisol', 'serum cortisol': 'cortisol',
        'acth': 'acth', 'adrenocorticotropic hormone': 'acth',
        'pth': 'pth', 'parathyroid hormone': 'pth',
        'growth hormone': 'growth_hormone', 'gh': 'growth_hormone',
        'igf-1': 'igf_1', 'insulin like growth factor 1': 'igf_1',
        'dheas': 'dheas', 'dhea sulfate': 'dheas',
        'beta hcg': 'beta_hcg', 'bhcg': 'beta_hcg',
        'amh': 'amh', 'anti mullerian hormone': 'amh',
        
        # ===== Vitamins / Nutrition =====
        'vitamin d': 'vitamin_d', '25 oh vitamin d': 'vitamin_d',
        'vitamin b12': 'vitamin_b12', 'b12': 'vitamin_b12',
        'folate': 'folate', 'folic acid': 'folate',
        'ferritin': 'ferritin',
        'iron': 'serum_iron', 'serum iron': 'serum_iron',
        'tibc': 'tibc', 'total iron binding capacity': 'tibc',
        'transferrin saturation': 'transferrin_saturation', 'iron saturation': 'transferrin_saturation',
        'zinc': 'zinc', 'copper': 'copper', 'selenium': 'selenium',
        'prealbumin': 'prealbumin',
        
        # ===== Urine Tests =====
        'urinalysis': 'urine_routine_examination', 'urine routine': 'urine_routine_examination',
        'urine microscopy': 'urine_microscopy', 'urine sediment': 'urine_microscopy',
        'urine culture': 'urine_culture_sensitivity',
        'urine specific gravity': 'urine_specific_gravity', 'usg': 'urine_specific_gravity',
        'urine ph': 'urine_ph',
        'urine pregnancy test': 'urine_pregnancy_test',
        'urine drug screen': 'urine_drug_screen',
        
        # ===== Serology / Infectious Disease =====
        'hiv': 'hiv', 'hiv 1': 'hiv', 'hiv 2': 'hiv',
        'hbsag': 'hbsag', 'hepatitis b surface antigen': 'hbsag',
        'anti hcv': 'anti_hcv', 'hepatitis c antibody': 'anti_hcv',
        'dengue': 'dengue_ns1', 'dengue ns1': 'dengue_ns1',
        'covid': 'covid_19_pcr', 'covid 19': 'covid_19_pcr',
        'widal': 'widal_test', 'widal test': 'widal_test',
        'vdrl': 'vdrl',
        'malaria': 'malaria_parasite', 'mp': 'malaria_parasite',
        'mantoux': 'mantoux_test', 'ppd': 'mantoux_test',
        
        # ===== Autoimmune =====
        'ana': 'ana', 'antinuclear antibody': 'ana',
        'rf': 'rheumatoid_factor', 'rheumatoid factor': 'rheumatoid_factor',
        'anti ccp': 'anti_ccp',
        'crp': 'crp', 'c-reactive protein': 'crp',
        'hs crp': 'hs_crp', 'high sensitivity crp': 'hs_crp',
        
        # ===== Tumor Markers =====
        'psa': 'psa', 'prostate specific antigen': 'psa',
        'cea': 'cea', 'carcinoembryonic antigen': 'cea',
        'afp': 'afp', 'alpha fetoprotein': 'afp',
        'ca 125': 'ca_125', 'ca125': 'ca_125',
        'ca 19-9': 'ca_19_9', 'ca19-9': 'ca_19_9',
        
        # ===== Fertility =====
        'semen analysis': 'semen_analysis', 'sperm count': 'semen_analysis',
        
        # ===== Body Fluids =====
        'csf': 'csf_analysis', 'cerebrospinal fluid': 'csf_analysis',
        'pleural fluid': 'pleural_fluid_analysis',
        'ascitic fluid': 'ascitic_fluid_analysis',
        'synovial fluid': 'synovial_fluid_analysis',
    }
    
    # Step 1: Check exact match in aliases
    if normalized in aliases:
        return aliases[normalized]
    
    # Step 2: Check if normalized contains any alias as substring
    for alias, standard in aliases.items():
        if alias in normalized or normalized in alias:
            return standard
    
    # Step 3: Check partial word match
    words = normalized.split()
    for alias, standard in aliases.items():
        alias_words = alias.split()
        for word in words:
            if word in alias_words or any(aw in word for aw in alias_words):
                return standard
    
    # Step 4: Return None if not found (will use default explanation)
    return None


# ==========================================================================
# REFERENCE RANGE FUNCTION
# ==========================================================================

def get_normal_range(test_name: Optional[str]) -> str:
    """Get the normal reference range for a test."""
    # Handle None input
    if not test_name:
        return "Reference range varies by laboratory"
    
    standardized = normalize_test_name(test_name)
    
    if not standardized:
        return "Reference range varies by laboratory"
    
    # Reference ranges dictionary
    ranges = {
        # Hematology
        'hemoglobin': '13.5-17.5 g/dL (men), 12.0-15.5 g/dL (women)',
        'wbc_count': '4.0-11.0 x10^3/uL',
        'platelet_count': '150-400 x10^3/uL',
        'rbc_count': '4.5-5.9 x10^6/uL (men), 4.0-5.2 x10^6/uL (women)',
        'hematocrit': '41-53% (men), 36-46% (women)',
        'mcv': '80-100 fL',
        'mch': '27-33 pg',
        'mchc': '32-36 g/dL',
        'rdw': '11.5-14.5%',
        'esr': '0-20 mm/hr (men), 0-30 mm/hr (women)',
        
        # Coagulation
        'pt': '11-13.5 seconds',
        'inr': '0.8-1.2',
        'aptt': '25-35 seconds',
        'fibrinogen': '200-400 mg/dL',
        'd_dimer': '<500 ng/mL',
        
        # Diabetes
        'fasting_blood_sugar': '70-99 mg/dL',
        'random_blood_sugar': '<140 mg/dL',
        'ppbs': '<140 mg/dL',
        'hba1c': '4.0-5.6%',
        'ogtt': '<140 mg/dL at 2 hours',
        
        # Kidney Function
        'serum_creatinine': '0.6-1.2 mg/dL (women), 0.7-1.4 mg/dL (men)',
        'bun': '7-20 mg/dL',
        'uric_acid': '2.5-7.0 mg/dL',
        'egfr': '≥90 mL/min/1.73m²',
        'sodium': '135-145 mEq/L',
        'potassium': '3.5-5.0 mEq/L',
        'chloride': '98-106 mEq/L',
        'bicarbonate': '22-26 mEq/L',
        'calcium': '8.5-10.5 mg/dL',
        'phosphorus': '2.5-4.5 mg/dL',
        'magnesium': '1.7-2.6 mg/dL',
        
        # Liver Function
        'total_bilirubin': '0.3-1.2 mg/dL',
        'direct_bilirubin': '0.0-0.3 mg/dL',
        'indirect_bilirubin': '0.2-0.8 mg/dL',
        'alt_sgpt': '10-40 U/L',
        'ast_sgot': '10-40 U/L',
        'alp': '44-147 U/L',
        'ggt': '9-60 U/L',
        'total_protein': '6.0-8.3 g/dL',
        'albumin': '3.5-5.0 g/dL',
        'ag_ratio': '1.0-2.0',
        
        # Lipid Profile
        'total_cholesterol': '<200 mg/dL',
        'hdl_cholesterol': '>40 mg/dL (men), >50 mg/dL (women)',
        'ldl_cholesterol': '<100 mg/dL',
        'triglycerides': '<150 mg/dL',
        
        # Cardiac Markers
        'troponin_i': '<0.04 ng/mL',
        'troponin_t': '<0.01 ng/mL',
        'ck_mb': '<5 ng/mL',
        'bnp': '<100 pg/mL',
        'nt_probnp': '<300 pg/mL',
        'homocysteine': '5-15 µmol/L',
        
        # Thyroid
        'tsh': '0.4-4.5 mIU/L',
        'free_t3': '2.3-4.2 pg/mL',
        'free_t4': '0.8-1.8 ng/dL',
        'anti_tpo': '<35 IU/mL',
        
        # Hormones
        'testosterone': '300-1000 ng/dL (men), 15-70 ng/dL (women)',
        'prolactin': '2-18 ng/mL (men), 2-29 ng/mL (women)',
        'cortisol': '5-25 µg/dL (8 AM)',
        'lh': '5-25 mIU/mL (women), 1-10 mIU/mL (men)',
        'fsh': '4-30 mIU/mL (women), 1-12 mIU/mL (men)',
        'pth': '15-65 pg/mL',
        'amh': '1.0-3.5 ng/mL',
        
        # Vitamins
        'vitamin_d': '30-100 ng/mL',
        'vitamin_b12': '200-900 pg/mL',
        'folate': '3-16 ng/mL',
        'ferritin': '30-300 ng/mL (men), 12-150 ng/mL (women)',
        'serum_iron': '60-170 µg/dL (men), 50-150 µg/dL (women)',
        'tibc': '250-400 µg/dL',
        'transferrin_saturation': '20-50%',
        
        # Autoimmune
        'ana': 'Negative (<1:40)',
        'crp': '<5 mg/L',
        'hs_crp': '<1.0 mg/L',
        'rheumatoid_factor': '<15 IU/mL',
        
        # Urine
        'urine_specific_gravity': '1.005-1.030',
        'urine_ph': '4.5-8.0',
        'urine_protein': '<150 mg/day',
        'microalbuminuria': '<30 mg/day',
    }
    
    return ranges.get(standardized, "Reference range varies by laboratory")


# ==========================================================================
# MAIN EXPLANATION FUNCTION
# ==========================================================================

def get_explanation(
    test_name: str,
    value=None,
    status: Optional[str] = None,
    unit=None,
    gender=None,
    age=None
) -> Dict[str, str]:

    standardized_name = normalize_test_name(test_name)

    # Step 2: If not found, return default explanation
    if not standardized_name:
        default = DEFAULT_EXPLANATION.copy()

        default["meaning"] = default["meaning"].format(
            test_name=test_name,
            status=status or "available"
        )

        return default
    
    # Step 3: Determine status if not provided but value is
    if status is None and value is not None:
        # Auto-determine status based on reference ranges for common tests
        auto_ranges = {
            'hemoglobin': (13.5, 17.5),
            'wbc_count': (4.0, 11.0),
            'platelet_count': (150, 400),
            'fasting_blood_sugar': (70, 100),
            'serum_creatinine': (0.7, 1.3),
            'total_cholesterol': (125, 200),
            'ldl_cholesterol': (0, 100),
            'hdl_cholesterol': (40, 100),
            'triglycerides': (0, 150),
            'sodium': (135, 145),
            'potassium': (3.5, 5.0),
            'calcium': (8.5, 10.5),
            'alt_sgpt': (10, 40),
            'ast_sgot': (10, 40),
            'tsh': (0.4, 4.5),
        }
        
        if standardized_name in auto_ranges:
            low, high = auto_ranges[standardized_name]
            try:
                val = float(value)
                if val < low:
                    status = "Low"
                elif val > high:
                    status = "High"
                else:
                    status = "Normal"
            except (ValueError, TypeError):
                status = "Normal"
        else:
            status = "Normal"
    
    # Step 4: Standardize the status string
    status_key = None
    if status:
        status_lower = str(status).lower()
        if 'low' in status_lower:
            status_key = "Low"
        elif 'high' in status_lower:
            status_key = "High"
        elif 'normal' in status_lower:
            status_key = "Normal"
    
    if not status_key:
        status_key = "Normal"
    
    # Step 5: Get explanation from knowledge base
    if standardized_name in MEDICAL_KNOWLEDGE_BASE:
        if status_key in MEDICAL_KNOWLEDGE_BASE[standardized_name]:
            return MEDICAL_KNOWLEDGE_BASE[standardized_name][status_key]
    
    # Step 6: Fallback to default explanation
    default = DEFAULT_EXPLANATION.copy()
    default["meaning"] = default["meaning"].format(
        test_name=test_name.capitalize(), 
        status=status_key
    )
    return default

# ==========================================================================
# BATCH EXPLANATION FUNCTION
# ==========================================================================

def get_batch_explanations(tests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
  
    results = []
    for test in tests:
        explanation = get_explanation(
            test_name=test.get('test_name', ''),
            value=test.get('value'),
            status=test.get('status', 'Normal'),
            unit=test.get('unit'),
            gender=test.get('gender'),
            age=test.get('age')
        )
        
        enriched_test = {
            'test_name': test.get('test_name'),
            'canonical_name': normalize_test_name(test.get('test_name', '')),
            'value': test.get('value'),
            'unit': test.get('unit'),
            'reference_range': get_normal_range(test.get('test_name', '')),
            'status': test.get('status', 'Normal'),
            'clinical_meaning': explanation.get('meaning', ''),
            'possible_causes': explanation.get('causes', ''),
            'clinical_effects': explanation.get('effects', ''),
            'recommendations': explanation.get('solution', '')
        }
        results.append(enriched_test)
    
    return results


# ==========================================================================
# CATEGORY FUNCTION
# ==========================================================================

def get_test_category(test_name: Optional[str]) -> str:
    """Return the category of a test."""
    if not test_name:
        return 'General'
    
    standardized = normalize_test_name(test_name)
    
    if not standardized:
        return 'General'
    
    categories = {
        'cbc': 'Hematology', 'hemoglobin': 'Hematology', 'hematocrit': 'Hematology',
        'rbc_count': 'Hematology', 'wbc_count': 'Hematology', 'platelet_count': 'Hematology',
        'pt': 'Coagulation', 'inr': 'Coagulation', 'aptt': 'Coagulation',
        'fasting_blood_sugar': 'Diabetes', 'hba1c': 'Diabetes',
        'serum_creatinine': 'Kidney Function', 'bun': 'Kidney Function', 'egfr': 'Kidney Function',
        'sodium': 'Electrolytes', 'potassium': 'Electrolytes', 'calcium': 'Electrolytes',
        'alt_sgpt': 'Liver Function', 'ast_sgot': 'Liver Function', 'total_bilirubin': 'Liver Function',
        'total_cholesterol': 'Lipid Profile', 'triglycerides': 'Lipid Profile',
        'troponin_i': 'Cardiac Markers', 'bnp': 'Cardiac Markers',
        'tsh': 'Thyroid Function', 'free_t4': 'Thyroid Function',
        'testosterone': 'Hormones', 'cortisol': 'Hormones', 'prolactin': 'Hormones',
        'vitamin_d': 'Nutrition', 'vitamin_b12': 'Nutrition', 'ferritin': 'Nutrition',
        'ana': 'Autoimmune', 'rheumatoid_factor': 'Autoimmune', 'crp': 'Inflammation',
        'urine_routine_examination': 'Urinalysis', 'urine_culture_sensitivity': 'Urinalysis',
        'hiv': 'Infectious Disease', 'hbsag': 'Infectious Disease',
        'psa': 'Tumor Markers', 'cea': 'Tumor Markers', 'afp': 'Tumor Markers',
        'semen_analysis': 'Fertility',
    }
    
    if standardized and standardized in categories:
        return categories[standardized]
    return 'General'


# ==========================================================================
# GET ALL SUPPORTED TESTS FUNCTION
# ==========================================================================

def get_all_test_names() -> List[str]:
    """
    Return list of all supported standard test names.
    
    Returns:
        List of canonical test names
    """
    return list(MEDICAL_KNOWLEDGE_BASE.keys())


# ==========================================================================
# SEARCH FUNCTION
# ==========================================================================

def search_test(query: str) -> List[Dict[str, str]]:
    """
    Search for tests by name or alias.
    
    Args:
        query: Search query string
    
    Returns:
        List of matching tests with canonical_name and original_alias
    """
    query_lower = query.lower().strip()
    results = []
    
    # Search in knowledge base keys
    for test_name in MEDICAL_KNOWLEDGE_BASE.keys():
        if query_lower in test_name:
            results.append({
                'canonical_name': test_name,
                'matched_as': test_name,
                'category': get_test_category(test_name)
            })
    
    # Search in aliases
    aliases_dict = {
        'hb': 'hemoglobin', 'hgb': 'hemoglobin', 'wbc': 'wbc_count', 
        'plt': 'platelet_count', 'rbc': 'rbc_count', 'hct': 'hematocrit',
        'alt': 'alt_sgpt', 'ast': 'ast_sgot', 'ldl': 'ldl_cholesterol',
        'hdl': 'hdl_cholesterol', 'tsh': 'tsh', 'psa': 'psa',
    }
    
    for alias, canonical in aliases_dict.items():
        if query_lower == alias or alias in query_lower:
            if canonical not in [r['canonical_name'] for r in results]:
                results.append({
                    'canonical_name': canonical,
                    'matched_as': alias,
                    'category': get_test_category(canonical)
                })
    
    return results


# ==========================================================================
# DISCLAIMER
# ==========================================================================

DISCLAIMER = """
DISCLAIMER: This medical knowledge base is for educational purposes only. 
This information is not a substitute for professional medical advice, diagnosis, or treatment. 
Always consult your healthcare provider for medical concerns.
"""