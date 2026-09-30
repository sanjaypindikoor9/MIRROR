import time

import onnxruntime as ort


class MirrorModelRunner:

    def __init__(self, model_path=None):

        self.model_path = model_path
        self.session = None

        if model_path:
            self.load_model(model_path)

    # ==========================================
    # LOAD MODEL
    # ==========================================

    def load_model(self, model_path):

        print("\nMIRROR AI MODEL")
        print("================")

        print(f"Loading: {model_path}")

        available = ort.get_available_providers()

        print("\nAvailable execution providers:")

        for provider in available:
            print(f"  ✓ {provider}")

        self.session = ort.InferenceSession(
            model_path,
            providers=available
        )

        self.model_path = model_path

        print("\n✓ Model loaded successfully.")

    # ==========================================
    # MODEL INFORMATION
    # ==========================================

    def get_model_info(self):

        if self.session is None:
            return None

        return {
            "model": self.model_path,
            "providers": self.session.get_providers(),
            "inputs": self.get_inputs(),
            "outputs": self.get_outputs()
        }

    # ==========================================
    # INPUTS
    # ==========================================

    def get_inputs(self):

        if self.session is None:
            return []

        return [
            {
                "name": node.name,
                "shape": node.shape,
                "type": node.type
            }
            for node in self.session.get_inputs()
        ]

    # ==========================================
    # OUTPUTS
    # ==========================================

    def get_outputs(self):

        if self.session is None:
            return []

        return [
            {
                "name": node.name,
                "shape": node.shape,
                "type": node.type
            }
            for node in self.session.get_outputs()
        ]

    # ==========================================
    # INFERENCE
    # ==========================================

    def run(self, inputs):

        if self.session is None:

            raise RuntimeError(
                "No ONNX model loaded."
            )

        start_time = time.perf_counter()

        outputs = self.session.run(
            None,
            inputs
        )

        end_time = time.perf_counter()

        inference_time = (
            end_time - start_time
        ) * 1000

        return {
            "outputs": outputs,
            "inference_time_ms": round(
                inference_time,
                2
            )
        }

    # ==========================================
    # STATUS
    # ==========================================

    def is_loaded(self):

        return self.session is not None


# ==============================================
# TEST
# ==============================================

if __name__ == "__main__":

    print(
        "\nMIRROR ONNX MODEL RUNTIME"
    )

    print(
        "========================="
    )

    print(
        "\nAvailable execution providers:"
    )

    for provider in ort.get_available_providers():

        print(
            f"  ✓ {provider}"
        )

    runner = MirrorModelRunner()

    print(
        "\nModel loaded:"
    )

    print(
        f"  {runner.is_loaded()}"
    )

    print(
        "\nMIRROR model runtime ready."
    )