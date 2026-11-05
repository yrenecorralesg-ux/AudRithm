"""Generar ocho páginas de referencia con evidencia local real."""
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle
from audrithm.reporting import SECTIONS, report_markdown
from audrithm.visualization import summary


def build():
    results = ROOT / "results"
    frame = pd.read_csv(results / "experiment_results.csv")
    metadata = json.loads((results / "experiment_metadata.json").read_text(encoding="utf-8"))
    qa = json.loads((results / "qa_results.json").read_text(encoding="utf-8"))
    output = ROOT / "output" / "pdf"
    output.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="AudTitle", fontSize=22, leading=27, textColor=colors.HexColor("#103d30"), spaceAfter=18))
    styles.add(ParagraphStyle(name="AudBody",fontSize=10,leading=15,spaceAfter=12))
    styles.add(ParagraphStyle(name="AudNote",fontSize=8,leading=11,textColor=colors.HexColor("#536878"),spaceAfter=10))
    story = []

    def para(text,style="AudBody"):
        story.append(Paragraph(escape(text).replace("\n","<br/>"),styles[style]))

    for index,(title,filename) in enumerate(SECTIONS,1):
        if index>1:
            story.append(PageBreak())
        para("AudRithm / Equipo 5 / Bitácora 1", "AudNote")
        para(f"{index}. {title}","AudTitle")
        if index==1:
            para("BORRADOR ASISTIDO POR IA · REVISIÓN ACADÉMICA PENDIENTE", "AudNote")
            para("Maestría en Tecnologías de la Información · Análisis y Diseño de Algoritmos · Cohorte X, 2026-III. Integrantes: nombres y aprobación pendientes.")
        text = (ROOT/"docs"/filename).read_text(encoding="utf-8").replace("**","").replace("`","")
        # Reservar espacio para evidencia en páginas 5 y 6.
        paragraphs = text.split("\n\n")
        if index==5:
            paragraphs = paragraphs[:2]
        if index==6:
            paragraphs = paragraphs[:1]
        for paragraph in paragraphs:
            para(paragraph)
        if index==4:
            para(f"Ejecución archivada: {qa['tests']} casos Pytest, {qa['passed']} aprobados, {qa['failures']} fallidos, {qa['errors']} errores; duración {qa['duration_s']:.3f} s. Fecha UTC: {qa['date']}.")
            para(f"Commit: {qa.get('commit') or 'no disponible durante la ejecución'}. SHA-256 del código: {qa['source_sha256']}.","AudNote")
        if index==5:
            table = summary(frame)
            data = [["n","Kadane (ms)","Bruta (ms)","Razón K","Razón B"]]
            for n,row in table.iterrows():
                data.append([str(n),f"{row['Kadane']/1e6:.5f}",f"{row['Fuerza bruta']/1e6:.3f}",
                             "-" if pd.isna(row['Razón Kadane']) else f"{row['Razón Kadane']:.2f}",
                             "-" if pd.isna(row['Razón Fuerza bruta']) else f"{row['Razón Fuerza bruta']:.2f}"])
            grid = Table(data,colWidths=[2*cm,3.3*cm,3.3*cm,2.5*cm,2.5*cm],repeatRows=1)
            grid.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#103d30")),("TEXTCOLOR",(0,0),(-1,0),colors.white),
                                     ("FONTSIZE",(0,0),(-1,-1),9),("BOTTOMPADDING",(0,0),(-1,-1),9),
                                     ("TOPPADDING",(0,0),(-1,-1),9),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.HexColor("#edf5f1"),colors.white])]))
            story.extend([grid,Spacer(1,14)])
            para(f"Entorno: Python {metadata['python']}; {metadata['os']}; procesador: {metadata['processor']}. Fecha UTC: {metadata['date']}.","AudNote")
            para("Dependencias: " + "; ".join(f"{k} {v}" for k,v in metadata['dependencies'].items()),"AudNote")
        if index==6:
            for name in ("normal","loglog"):
                story.append(Image(str(results/f"timing_{name}.png"),width=15*cm,height=7.5*cm))
            para("Figuras derivadas del CSV archivado. Interpretación y conclusión final pendientes del equipo; no constituyen demostración matemática.","AudNote")
        if index==8:
            para("Repositorio: https://github.com/yrenecorralesg-ux/AudRithm", "AudNote")
            para("Fuente académica: Asignación de proyectos por equipo y Bitácora 1, Profa. Msc. Sosa, Cohorte X, 2026-III; PDF suministrado por el usuario. La solicitud completa de desarrollo se conserva en docs/user_request.txt.","AudNote")

    def footer(canvas,doc):
        canvas.setStrokeColor(colors.HexColor("#059669"))
        canvas.line(2*cm,1.5*cm,19*cm,1.5*cm)
        canvas.setFont("Helvetica",8)
        canvas.drawString(2*cm,1.1*cm,"AudRithm · Borrador para revisión del equipo · 2026-11-05")
        canvas.drawRightString(19*cm,1.1*cm,str(doc.page))

    SimpleDocTemplate(str(output/"Equipo_5_Bitacora1.pdf"),pagesize=(21*cm,29.7*cm),rightMargin=2*cm,leftMargin=2*cm,topMargin=1.8*cm,bottomMargin=2*cm,
                      title="AudRithm - Bitácora 1 (borrador)",author="Referencia asistida por IA; revisión del equipo pendiente").build(story,onFirstPage=footer,onLaterPages=footer)
    (ROOT/"docs"/"bitacora1.md").write_text(report_markdown(),encoding="utf-8")
    print(output/"Equipo_5_Bitacora1.pdf")

if __name__ == "__main__":
    build()
