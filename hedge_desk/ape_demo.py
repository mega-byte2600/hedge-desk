"""APE PFAC PSSM 5 demo payload for the public web route.

This module intentionally contains only non-sensitive demonstration data. It maps
Michael Bolton's APE agreement competencies to a leadership-ready PFAC playbook.
"""

from __future__ import annotations


SUPABASE_EDGE_URL = "https://pwwzqijuphsmlryhtphx.supabase.co/functions/v1/ape-pfac-demo"


def build_ape_pfac_demo():
    return {
        "schema_version": "ape-pfac-pssm5-demo-1",
        "project": {
            "title": "PFAC-PSSM Leadership Playbook",
            "subtitle": "PSSM 5 demonstration: Patient and Family Engagement through PFACs, co-design, co-production, and learning health system action.",
            "scope": "PSSM 5 only. PSSM 1 through 4 are intentionally excluded from this demo layer.",
            "thesis": "A health system can complete the transaction and still deliver a poor experience. The playbook uses the Chick-fil-A versus McDonald's service lens to move from transactional care to guided, respectful, co-designed patient experience.",
            "supabase_edge_url": SUPABASE_EDGE_URL,
        },
        "competencies": [
            {
                "id": "ceph-4",
                "label": "CEPH 4",
                "agreement_text": "Interpret results of data analysis for public health research, policy, or practice.",
                "demo_proof": "The evidence layer converts PFAC, patient engagement, co-production, and LHS literature into practical leadership claims, source validation, and deployment actions.",
            },
            {
                "id": "ceph-7",
                "label": "CEPH 7",
                "agreement_text": "Assess population needs, assets, and capacities that affect communities' health.",
                "demo_proof": "PFACs are used as a structured mechanism to identify patient and family needs, barriers, assets, trust gaps, and experience breakdowns.",
            },
            {
                "id": "ceph-16",
                "label": "CEPH 16",
                "agreement_text": "Apply leadership and/or management principles to address a relevant issue.",
                "demo_proof": "The playbook gives leaders a repeatable model to launch, sponsor, govern, document, and sustain PFAC work tied to PSSM 5.",
            },
            {
                "id": "ceph-21",
                "label": "CEPH 21",
                "agreement_text": "Integrate perspectives from other sectors and/or professions to promote and advance population health.",
                "demo_proof": "The model integrates patients, families, clinicians, quality teams, patient experience staff, executives, and implementation partners.",
            },
            {
                "id": "dartmouth-4",
                "label": "Dartmouth Program-Specific Competency 4",
                "agreement_text": "Compare two approaches to engaging target populations in decision making, design, governance, and delivery of services, including impacts on quality, safety, equity, and value.",
                "demo_proof": "The demo compares transactional engagement to co-designed engagement and shows how PFACs convert patient voice into learning health system action.",
            },
        ],
        "evidence": [
            {
                "source": "AHRQ PSSM Domain 5",
                "claim": "PSSM 5 centers Patient and Family Engagement, including PFAC input on safety.",
                "leadership_use": "Controls scope and prevents the toolkit from drifting into unrelated PSSM domains.",
            },
            {
                "source": "Oldfield et al., 2019",
                "claim": "PFACs are established structures for patient, family, and community engagement in health care and research.",
                "leadership_use": "Supports PFAC design, recruitment, representation, governance, and documentation standards.",
            },
            {
                "source": "Sharma et al., 2017",
                "claim": "Patient advisors can contribute to healthcare outcomes when advisory work is connected to implementation and measurement.",
                "leadership_use": "Keeps the PFAC focused on action, not symbolic participation.",
            },
            {
                "source": "Batalden et al., 2016",
                "claim": "Healthcare service is co-produced through relationships and activities between professionals and the people served.",
                "leadership_use": "Frames the PFAC as co-production infrastructure, not a courtesy committee.",
            },
            {
                "source": "Batalden and Foster, 2021",
                "claim": "Quality improvement has moved from assurance alone toward co-produced service value.",
                "leadership_use": "Connects PFAC deployment to leadership, quality, patient experience, and service redesign.",
            },
            {
                "source": "Oliver et al., 2019",
                "claim": "Feed-forward and feedback processes can turn patient-reported data into intelligent action and decision-making.",
                "leadership_use": "Makes the learning health system loop practical: capture, interpret, act, document, reassess.",
            },
        ],
        "deployment_steps": [
            "Lock PSSM 5 scope and document why PSSM 1 through 4 are excluded from this demo layer.",
            "Recruit PFAC members for lived experience, trust gaps, safety concerns, and care journey breakdowns.",
            "Co-design the patient experience standard before implementation decisions are finalized.",
            "Assign leadership ownership, review patient/family themes, choose actions, and document follow-through.",
            "Reassess PFAC maturity and patient experience impact quarterly.",
        ],
        "playbook_outputs": [
            "PFAC current-state assessment",
            "PFAC maturity model",
            "PSSM 5 evidence map",
            "Leadership deployment checklist",
            "Co-design meeting guide",
            "You said, we did action tracker",
            "Quarterly reassessment dashboard",
        ],
        "references": [
            "Agency for Healthcare Research and Quality. Resources by the CMS Patient Safety Structural Measure Domains. AHRQ. Accessed September 7, 2026.",
            "Oldfield BJ, Harrison MA, Genao I, et al. Patient, family, and community advisory councils in health care and research: a systematic review. J Gen Intern Med. 2019;34(7):1292-1303. doi:10.1007/s11606-018-4565-9",
            "Sharma AE, Knox M, Mleczko VL, Olayiwola JN. The impact of patient advisors on healthcare outcomes: a systematic review. BMC Health Serv Res. 2017;17:693. doi:10.1186/s12913-017-2630-4",
            "Batalden M, Batalden P, Margolis P, et al. Coproduction of healthcare service. BMJ Qual Saf. 2016;25(7):509-517. doi:10.1136/bmjqs-2015-004315",
            "Batalden P, Foster T. From assurance to coproduction: a century of improving the quality of health-care service. Int J Qual Health Care. 2021;33(suppl 2):ii10-ii14. doi:10.1093/intqhc/mzab059",
            "Oliver BJ, Nelson EC, Kerrigan CL. Turning feed-forward and feedback processes on patient-reported data into intelligent action and informed decision-making: case studies and principles. Med Care. 2019;57(suppl 5 suppl 1):S31-S37. doi:10.1097/MLR.0000000000001088",
        ],
    }
