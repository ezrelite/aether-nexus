"""
Aether Brain Module.
Handles Groq API interactions and Red Team Logic.
"""
import json
import streamlit as st
from groq import Groq
from .config import GROQ_API_KEY

def get_groq_response(messages, model_id="llama-3.1-8b-instant"):
    """
    Connects to Groq's high-speed inference engine.
    Supports dynamic model selection (User Control).
    """
    client = Groq(api_key=GROQ_API_KEY)
    
    # Primary Model (User Selected)
    primary_model = model_id
    
    # Fallback Model (Dumb but Cheap)
    fallback_model = "llama-3.1-8b-instant"

    try:
        completion = client.chat.completions.create(
            model=primary_model, 
            messages=messages,
            temperature=0.6,
            max_tokens=1024,
            response_format={"type": "json_object"}
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        error_msg = str(e).lower()
        if "rate limit" in error_msg or "429" in error_msg:
            print(f"⚠️ GROQ 429: Switching to Fallback from {primary_model} to {fallback_model}...")
            try:
                # Retry with Fallback API
                completion = client.chat.completions.create(
                    model=fallback_model, 
                    messages=messages,
                    temperature=0.6,
                    max_tokens=1024,
                    response_format={"type": "json_object"}
                )
                return completion.choices[0].message.content
            except Exception as e2:
                # Both failed
                return json.dumps({"final_reply": f"CRITICAL BRAIN FAILURE (Both models exhausted): {str(e2)}"})
        
        return json.dumps({"final_reply": f"CONNECTION ERROR: {str(e)}"})

# --- RED TEAM LOGIC (Adversarial Mode) ---
def run_red_team_loop(user_input, status_container, model_id="llama-3.1-8b-instant"):
    """
    Executes the 3-Step Red Team Loop: Builder -> Destroyer -> Refiner.
    """
    try:
        # Step 1: The Builder (Agent A)
        status_container.markdown(f"🏗️ *Step 1: The Builder is designing ({model_id})...*")
        builder_prompt = f"You are an expert architect. Propose a concrete solution for: {user_input}. Return JSON with key 'plan'."
        builder_res = get_groq_response([{"role": "user", "content": builder_prompt}], model_id=model_id)
        try:
            plan_a = json.loads(builder_res).get("plan", builder_res)
        except:
            plan_a = builder_res
        
        with st.expander("Step 1: Initial Plan (Click to View)", expanded=False):
            if isinstance(plan_a, dict):
                for k, v in plan_a.items():
                    st.markdown(f"**{k}:** {v}")
            elif isinstance(plan_a, list):
                for item in plan_a:
                    st.markdown(f"- {item}")
            else:
                st.write(plan_a)

        # Step 2: The Destroyer (Agent B)
        status_container.markdown("💣 *Step 2: The Destroyer is finding fatal flaws...*")
        # Updated Prompt to avoid hallucinating Physics flaws in digital tasks
        destroyer_prompt = f"You are a critical reviewer. Look at this plan: {plan_a}. Critique it pragmatically. If it's a simple task, APPROVE it. If complex, find risks. Return JSON with key 'fatal_flaws' (list)."
        destroyer_res = get_groq_response([{"role": "user", "content": destroyer_prompt}])
        
        try:
            critique_data = json.loads(destroyer_res)
            critique = critique_data.get("fatal_flaws", critique_data)
        except:
            critique = destroyer_res
            
        with st.expander("Step 2: Critique (Click to View)", expanded=False):
            if isinstance(critique, list):
                for flaw in critique:
                    st.error(f"**Critique**: {flaw}")
            else:
                st.write(critique)

        # Step 3: The Refiner (Redemption)
        status_container.markdown("🛠️ *Refining Solution (Step 3/3)...*")
        
        refiner_prompt = f"""
        ORIGINAL GOAL: {user_input}
        BUILDER'S PLAN: {plan_a}
        CRITIQUE: {critique}
        
        TASK:
        You are the Lead Engineer.
        1. Address the critique.
        2. Provide the final, polished plan.
        
        Return JSON ONLY:
        {{
            "final_solution": "Name of solution",
            "pivot_logic": "Why we adjusted",
            "execution_plan": ["Step 1", "Step 2", "Step 3"]
        }}
        """
        
        # Run the Refiner
        refiner_response = get_groq_response([{"role": "user", "content": refiner_prompt}])
        
        # Display the Final Result (Clean UI)
        st.markdown("### ✅ FINAL APPROVED PLAN")
        try:
            final_json = json.loads(refiner_response)
            
            # 1. Immediate UI Display
            st.success(f"**Pivot:** {final_json.get('final_solution', 'Solution')}")
            st.info(f"**Logic:** {final_json.get('pivot_logic', 'Logic')}")
            
            exec_plan = final_json.get('execution_plan', [])
            if isinstance(exec_plan, list):
                for i, step in enumerate(exec_plan, 1):
                    st.write(f"**{i}.** {step}")
            else:
                st.write(exec_plan)
                
            # 2. Construct Clean Markdown for History/Status
            final_md = f"""### ✅ FINAL APPROVED PLAN
**Pivot:** {final_json.get('final_solution')}

**Logic:** {final_json.get('pivot_logic')}

**Execution Plan:**
"""
            if isinstance(exec_plan, list):
                for i, step in enumerate(exec_plan, 1):
                    final_md += f"{i}. {step}\n"
            else:
                final_md += str(exec_plan)

            status_container.empty()
            return final_md
            
        except:
            st.write(refiner_response)
            return refiner_response

    except Exception as e:
        return f"RED TEAM ERROR: {str(e)}"
