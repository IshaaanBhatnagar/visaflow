from pydantic import BaseModel
from typing import Optional


class ColorConfig(BaseModel):
    partner1Name: str  # CSS variable name, e.g. "visa"
    partner1Hex: str  # e.g. "#1A1F71"
    partner1Light: str  # e.g. "#DBEAFE"
    partner2Name: Optional[str] = None
    partner2Hex: Optional[str] = None
    partner2Light: Optional[str] = None
    accentHex: str  # e.g. "#F7B600"
    accentLight: str  # e.g. "#FEF3C7"
    platformHex: str  # Clear green, "#16A34A"
    platformLight: str  # "#DCFCE7"


class Party(BaseModel):
    id: str  # e.g. "seller", "clear", "payfac"
    label: str  # e.g. "Seller", "Clear", "Visa PayFac"
    bgClass: str  # e.g. "bg-seller-light"
    textClass: str  # e.g. "text-seller"


class StatCard(BaseModel):
    value: str
    label: str
    description: str


class GapItem(BaseModel):
    bold: str
    text: str


class GapSection(BaseModel):
    headline: str
    body: str
    callout: str


class PartnerCard(BaseModel):
    partnerName: str
    partnerInitial: str
    colorClass: str  # e.g. "visa" or "mashreq"
    headline: str
    body: str


class Tab1Opportunity(BaseModel):
    headline: str
    subheadline: str
    statCards: list[StatCard]
    whatItSolves: list[GapItem]
    whatItDoesntSolve: GapSection
    quoteBanner: str
    partnerCards: list[PartnerCard]


class FlowNode(BaseModel):
    title: str
    subtitle: str
    parties: list[str]
    layer: str  # "compliance" or "payment"


class FlowNodeDetail(BaseModel):
    title: str
    subtitle: str
    parties: list[str]
    detail: str
    dataFlow: str


class ValidationStep(BaseModel):
    label: str


class DashboardStat(BaseModel):
    value: str
    label: str
    colorClass: str  # e.g. "gray-900", "primary", "positive"


class DashboardRow(BaseModel):
    cells: list[str]  # Raw HTML cells for flexibility


class Dashboard(BaseModel):
    iconBgClass: str  # e.g. "bg-primary"
    iconInitial: str
    title: str
    headerStats: Optional[list[str]] = None  # Optional summary stats in header
    stats: list[DashboardStat]
    tableHeaders: list[str]
    rows: list[DashboardRow]


class InvoiceLineItem(BaseModel):
    description: str
    qty: str
    rate: str
    amount: str


class InvoiceMockup(BaseModel):
    sellerName: str
    sellerAddress: str
    sellerTrn: str
    buyerName: str
    buyerAddress: str
    buyerTrn: str
    invoiceNumber: str
    invoiceDate: str
    dueDate: str
    lineItems: list[InvoiceLineItem]
    subtotal: str
    vatRate: str
    vatAmount: str
    total: str
    currency: str


class PhoneScreen(BaseModel):
    stepLabel: str
    contentHtml: str  # Pre-formatted HTML for inside the phone


class ReturnBullet(BaseModel):
    bold: str
    text: str


class ReturnCard(BaseModel):
    partnerName: str
    partnerInitial: str
    colorClass: str
    headline: str
    bullets: list[ReturnBullet]


class AdoptionCard(BaseModel):
    headline: str
    bullets: list[ReturnBullet]


class AlignmentCard(BaseModel):
    headline: str
    body: str


class Tab5Returns(BaseModel):
    headline: str
    subheadline: str
    returnCards: list[ReturnCard]
    adoptionCard: AdoptionCard
    alignmentCard: AlignmentCard


class SecurityCard(BaseModel):
    name: str
    description: str
    iconBgClass: str  # e.g. "bg-green-50"
    iconColorClass: str  # e.g. "text-positive"
    iconType: str  # "shield" or "lock"


class FootprintCard(BaseModel):
    country: str
    borderColorClass: str  # e.g. "border-orange-400"
    description: str


class InfraCard(BaseModel):
    title: str
    body: str


class Tab6Security(BaseModel):
    headline: str
    subheadline: str
    footprintHeadline: str
    footprintSubheadline: str
    footprintCards: list[FootprintCard]
    securityCards: list[SecurityCard]
    infraHeadline: str
    infraCards: list[InfraCard]


class DeckContent(BaseModel):
    pageTitle: str
    footerText: str
    navPartner1Name: str
    navPartner1Initial: str
    navPlatformName: str
    navPlatformInitial: str
    country: str
    currency: str

    colors: ColorConfig
    parties: list[Party]

    tab1: Tab1Opportunity

    sellerFlowNodes: dict[str, FlowNode]
    sellerValidationSteps: list[ValidationStep]
    buyerFlowNodes: dict[str, FlowNode]
    buyerValidationSteps: list[ValidationStep]
    nodeDetails: dict[str, FlowNodeDetail]

    sellerDashboard: Dashboard
    partnerDashboard: Dashboard
    buyerDashboard: Dashboard

    invoiceMockup: InvoiceMockup
    phoneScreens: list[PhoneScreen]

    tab5: Tab5Returns
    tab6: Tab6Security
