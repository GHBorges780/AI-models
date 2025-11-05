import nuke
import sys

def on_create():
    this = nuke.thisNode()
    inference = nuke.toNode(f"{this.name()}.Inference_S")
    this["gpuName"].setValue(inference["gpuName"].value())
    inference.forceValidate()
    is_enabled = inference["modelFile"].enabled()

    if sys.platform.lower() == "darwin":
        if not inference["useGPUIfAvailable"].enabled():
            this["useGPUIfAvailable"].setValue(False)
            this["useGPUIfAvailable"].setEnabled(False)

        this["halfPrecision"].setValue(False)
        this["halfPrecision"].setVisible(False)

    if not is_enabled:
        for k in this.knobs():
            this[k].setEnabled(False)

def check_knob_status():
    this = nuke.thisNode()
    inference = nuke.toNode(f"{this.name()}.Inference_S")
    is_enabled = inference["modelFile"].enabled()
    gizmo_enabled = this['useGPUIfAvailable'].enabled()

    # Ensure gizmos knobs are enabled/disabled
    if not gizmo_enabled and is_enabled:
        for k in this.knobs(): this[k].setEnabled(True)
    elif gizmo_enabled and not is_enabled:
        for k in this.knobs(): this[k].setEnabled(False)

def knob_changed():
    this = nuke.thisNode()
    if ('halfPrecision' in this.knobs()) and (sys.platform.lower() != "darwin"):
        this["halfPrecision"].setVisible(this["useGPUIfAvailable"].value())
    check_knob_status()
