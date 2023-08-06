import { fabric } from "fabric"
import FabricTool, { ConfigureCanvasProps } from "./fabrictool"

class RectTool extends FabricTool {
  isMouseDown: boolean = false
  fillColor: string = "#ffffff"
  strokeWidth: number = 10
  strokeColor: string = "#ffffff"
  currentRect: fabric.Rect = new fabric.Rect()
  currentStartX: number = 0
  currentStartY: number = 0

  configureCanvas({
    strokeWidth,
    strokeColor,
    fillColor,
  }: ConfigureCanvasProps): () => void {
    this._canvas.isDrawingMode = false
    this._canvas.selection = false
    this._canvas.forEachObject((o) => (o.selectable = o.evented = false))

    this.strokeWidth = strokeWidth
    this.strokeColor = strokeColor
    this.fillColor = fillColor

    this._canvas.on("mouse:down", (e: any) => this.onMouseDown(e))
    this._canvas.on("mouse:move", (e: any) => this.onMouseMove(e))
    this._canvas.on("mouse:up", (e: any) => this.onMouseUp(e))
    this._canvas.on("mouse:out", (e: any) => this.onMouseOut(e))
    return () => {
      this._canvas.off("mouse:down")
      this._canvas.off("mouse:move")
      this._canvas.off("mouse:up")
      this._canvas.off("mouse:out")
    }
  }

  onMouseDown(o: any) {
    let canvas = this._canvas
    this.isMouseDown = true
    let pointer = canvas.getPointer(o.e)
    this.currentStartX = pointer.x
    this.currentStartY = pointer.y
    this.currentRect = new fabric.Rect({
      left: this.currentStartX,
      top: this.currentStartY,
      originX: "left",
      originY: "top",
      width: pointer.x - this.currentStartX,
      height: pointer.y - this.currentStartY,
      stroke: this.strokeColor,
      strokeWidth: this.strokeWidth,
      fill: this.fillColor,
      transparentCorners: false,
      selectable: false,
      evented: false,
      strokeUniform: true,
      noScaleCache: false,
      angle: 0,
    })
    canvas.add(this.currentRect)
  }

  onMouseMove(o: any) {
    if (!this.isMouseDown) return
    let canvas = this._canvas
    let pointer = canvas.getPointer(o.e)
    if (this.currentStartX > pointer.x) {
      this.currentRect.set({ left: Math.abs(pointer.x) })
    }
    if (this.currentStartY > pointer.y) {
      this.currentRect.set({ top: Math.abs(pointer.y) })
    }
    this.currentRect.set({ width: Math.abs(this.currentStartX - pointer.x) })
    this.currentRect.set({ height: Math.abs(this.currentStartY - pointer.y) })
    this.currentRect.setCoords()
    canvas.renderAll()
  }

  onMouseUp(o: any) {
    this.isMouseDown = false
  }

  onMouseOut(o: any) {
    this.isMouseDown = false
  }
}

export default RectTool
