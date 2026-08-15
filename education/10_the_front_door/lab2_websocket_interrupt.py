"""Reference solution. Moved from the old education/labs tree."""
import asyncio
import json
import time

# 1. Stateful Agent Execution Loop with Interrupt Checkpoints
async def run_agent_graph(interrupt_event: asyncio.Event):
    print("[AGENT ENGINE] Starting multi-step graph execution...")
    nodes = ["Node 1: Context Analysis", "Node 2: Code Generation", "Node 3: Security Verification"]

    for idx, node_name in enumerate(nodes, start=1):
        # GRAPH NODE CHECKPOINT: Check for client interrupt signal
        if interrupt_event.is_set():
            print(f"\n[INTERRUPT HANDLER] [STOP] Interrupt Flag SET! Pausing graph execution at boundary before '{node_name}'.")

            print("[INTERRUPT HANDLER] Status: AGENT_INTERRUPTED_AWAITING_USER_INPUT")
            return {
                "status": "INTERRUPTED",
                "stopped_at_node": node_name,
                "completed_nodes": idx - 1
            }

        print(f"  [NODE EXECUTION] Running {node_name}...")
        await asyncio.sleep(0.1)  # Simulate node work latency

    print("[AGENT ENGINE] All graph nodes completed successfully.")
    return {"status": "COMPLETED", "completed_nodes": len(nodes)}

# 2. Simulated WebSocket Inbound Control Receiver Task
async def simulate_client_interrupt_receiver(interrupt_event: asyncio.Event, delay_seconds: float):
    await asyncio.sleep(delay_seconds)
    print(f"\n[WEBSOCKET CLIENT] Pushing Inbound Control Frame: 'INTERRUPT_TURN'")
    interrupt_event.set()

# 3. Main Orchestrator
async def main():
    print("=== STARTING WEBSOCKET INTERACTIVE INTERRUPTION LAB ===")
    
    # Test Scenario 1: Normal Uninterrupted Run
    print("\n--- SCENARIO 1: Uninterrupted Agent Execution ---")
    event_no_interrupt = asyncio.Event()
    res1 = await run_agent_graph(event_no_interrupt)
    print(f"Result: {res1}")

    # Test Scenario 2: Mid-Turn Client Interruption
    print("\n--- SCENARIO 2: Mid-Turn Client Interruption ---")
    event_with_interrupt = asyncio.Event()
    
    # Launch agent graph execution and client interrupt receiver concurrently
    agent_task = asyncio.create_task(run_agent_graph(event_with_interrupt))
    client_task = asyncio.create_task(simulate_client_interrupt_receiver(event_with_interrupt, delay_seconds=0.15))

    res2 = await asyncio.gather(agent_task, client_task)
    print(f"Result: {res2[0]}")

if __name__ == "__main__":
    asyncio.run(main())
