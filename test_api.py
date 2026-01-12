import asyncio
from src.nexus.planner import planner

async def main():
    print("Testing Planner module...")
    try:
        plan = await planner.generate_plan("Hello world")
        print("Plan generated successfully!")
        print(f"Reply: {plan.get('assistant_reply')}")
        print(f"Steps: {len(plan.get('execution_plan', []))}")
    except Exception as e:
        print(f"Planner failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
