"""Reference solution. Moved from the old education/labs tree."""
import json
import time
from typing import Dict, Any, List

# 1. Server-Driven UI (SDUI) Component Registry Protocol
def render_sdui_component_frame(component_name: str, props: Dict[str, Any]) -> Dict[str, Any]:
    """Serializes tool outputs into structured Server-Driven UI (SDUI) component payloads."""
    return {
        "type": "GENERATIVE_UI_FRAME",
        "component": component_name,
        "props": props,
        "timestamp": time.time()
    }

# 2. Stateful Human-in-the-Loop (HITL) Gate Engine
class AgentHITLEngine:
    """Manages pause/resume checkpoints and approval RPC handoffs."""
    def __init__(self):
        self.checkpoints: Dict[str, Dict[str, Any]] = {}

    def execute_action_with_hitl_gate(
        self, action_name: str, payload: Dict[str, Any], is_high_risk: bool
    ) -> Dict[str, Any]:
        print(f"\n[HITL GATE] Intercepted Action: '{action_name}' (High Risk: {is_high_risk})")
        
        # LOW RISK: Execute immediately
        if not is_high_risk:
            print("  [APPROVED] Low-risk action approved automatically.")
            return {"status": "EXECUTED", "action": action_name}

        # HIGH RISK: Pause graph and save state checkpoint
        approval_id = f"appr-{int(time.time() * 1000)}"
        self.checkpoints[approval_id] = {
            "action": action_name,
            "payload": payload,
            "status": "PAUSED_AWAITING_APPROVAL"
        }

        # Generate SDUI Approval Modal Component Frame
        sdui_frame = render_sdui_component_frame(
            component_name="HITLApprovalModal",
            props={
                "approval_id": approval_id,
                "action": action_name,
                "proposed_changes": payload,
                "warning": "CRITICAL: This action modifies persistent production state!"
            }
        )

        print(f"  [PAUSED] HIGH-RISK ACTION PAUSED! Created Checkpoint ID: {approval_id}")
        print(f"  [SDUI FRAME EMITTED TO FRONTEND UI]:\n{json.dumps(sdui_frame, indent=2)}")
        return {
            "status": "PAUSED",
            "approval_id": approval_id,
            "sdui_frame": sdui_frame
        }

    def resume_agent_execution(self, approval_id: str, decision: str) -> Dict[str, Any]:
        """RPC postback endpoint resuming agent graph after human approval."""
        print(f"\n[HITL RPC RESUME] Processing Human Clearance for ID: '{approval_id}' -> Decision: '{decision}'")
        
        if approval_id not in self.checkpoints:
            raise KeyError(f"Invalid Approval ID: '{approval_id}'")

        checkpoint = self.checkpoints[approval_id]

        if decision == "APPROVED":
            checkpoint["status"] = "APPROVED_AND_EXECUTED"
            print(f"  [APPROVED] Action '{checkpoint['action']}' AUTHORIZED by user. Graph execution resumed!")
            return {
                "status": "RESUMED_SUCCESS",
                "action": checkpoint["action"],
                "execution_result": "Database migration script applied successfully."
            }
        else:
            checkpoint["status"] = "REJECTED_BY_USER"
            print(f"  [REJECTED] Action '{checkpoint['action']}' REJECTED by user. Graph state aborted!")
            return {
                "status": "ABORTED",
                "action": checkpoint["action"],
                "reason": "Human operator rejected execution."
            }


if __name__ == "__main__":
    print("=== STARTING GENERATIVE UI & HITL APPROVAL GATE LAB ===")
    engine = AgentHITLEngine()

    # Scenario 1: Low-Risk Action (Auto Executed)
    engine.execute_action_with_hitl_gate(
        action_name="read_schema",
        payload={"table": "users"},
        is_high_risk=False
    )

    # Scenario 2: High-Risk Action (HITL Gate Pauses & Emits SDUI Frame)
    res_high_risk = engine.execute_action_with_hitl_gate(
        action_name="apply_db_migration",
        payload={"sql": "ALTER TABLE users DROP COLUMN legacy_auth_hash"},
        is_high_risk=True
    )

    # Extract approval_id from paused checkpoint
    appr_id = res_high_risk["approval_id"]

    # Scenario 3: Human Operator Approves Action via RPC Resume Postback
    engine.resume_agent_execution(approval_id=appr_id, decision="APPROVED")
