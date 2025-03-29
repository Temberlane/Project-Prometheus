import grpc
import distributed_ai_pb2
import distributed_ai_pb2_grpc

def query_node(node_address, text_input):
    channel = grpc.insecure_channel(node_address)
    stub = distributed_ai_pb2_grpc.NodeServiceStub(channel)
    response = stub.Predict(distributed_ai_pb2.PredictRequest(input_text=text_input))
    return response.prediction

def critique_node(node_address, node_id, prev_pred, rationale):
    channel = grpc.insecure_channel(node_address)
    stub = distributed_ai_pb2_grpc.NodeServiceStub(channel)
    response = stub.Critique(
        distributed_ai_pb2.CritiqueRequest(
            node_id=node_id,
            previous_prediction=prev_pred,
            rationale=rationale
        )
    )
    return response.critique

if __name__ == "__main__":
    text = "Bob Ross is still alive"
    pred_A = query_node("localhost:50052", text)
    pred_B = query_node("localhost:50053", text)
    critique_from_A = critique_node("localhost:50052", "node_B", pred_B, "Disagrees with relevant science.")
    critique_from_B = critique_node("localhost:50053", "node_A", pred_A, "Check the data for consistency.")

    with open("debate_log.txt", "a") as f:
        f.write("--- Debate Start ---\n")
        f.write(f"Node A says: {pred_A}\n")
        f.write(f"Node B says: {pred_B}\n")
        f.write(f"A critiques B: {critique_from_A}\n")
        f.write(f"B critiques A: {critique_from_B}\n")
        f.write("--- Debate End ---\n")