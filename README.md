# RAG-Project
=======
# 🎯 Système RAG - Retrieval-Augmented Generation

Système complet et intelligent de **Retrieval-Augmented Generation** pour interroger vos documents personnalisés avec l'IA locale.

---

## 📋 Table des matières

1. [Vue d'ensemble](#-vue-densemble)
2. [Architecture](#-architecture)
3. [Installation](#-installation)
4. [Utilisation](#-utilisation)
5. [Configuration](#-configuration)
6. [Fichiers du projet](#-fichiers-du-projet)
7. [Améliorations récentes](#-améliorations-récentes)
8. [Dépendances](#-dépendances)
9. [Dépannage](#-dépannage)

---

## 👁️ Vue d'ensemble

Ce projet implémente un système **RAG complet** qui:
- ✅ **Charge vos documents** (PDF, TXT) depuis le dossier `data/`
- ✅ **Les indexe intelligemment** dans une base vectorielle (Chroma DB)
- ✅ **Récupère le contexte pertinent** en fonction de votre question
- ✅ **Génère des réponses** avec l'IA locale (Ollama - phi3:latest)
- ✅ **Évalue la qualité** automatiquement avec RAGAS
- ✅ **Affiche les sources** d'où proviennent les réponses

### Flux de travail

```
📄 Documents (PDF/TXT)
         ⬇️
    🔍 Ingestion
         ⬇️
    ✂️ Chunking & Embedding
         ⬇️
    📊 Chroma DB (Vector Store)
         ⬇️
    ❓ Votre Question
         ⬇️
    🔎 Récupération (Top-K Documents)
         ⬇️
    🤖 Ollama LLM (Générer réponse)
         ⬇️
    📈 RAGAS (Évaluation optionnelle)
         ⬇️
    ✨ Réponse + Sources + Scores
```

---

## 📐 Architecture

```
RAG_Project/
├── 📁 data/                          # Documents source (PDF, TXT)
│   └── *.pdf, *.txt
├── 📁 db/
│   └── chroma_db/                   # Base de données vectorielle persistante
├── 📁 src/                          # Code source
│   ├── config.py                    # ⚙️ Configuration globale
│   ├── ingestion.py                 # 📥 Phase 1: Charger & indexer docs
│   ├── retrieval.py                 # 🔍 Phase 2: RAG + Mode interactif
│   ├── ragas_eval.py                # 📊 Évaluation RAGAS des réponses
│   ├── evaluation.py                # (Fichier legacy - peut être ignoré)
│   └── prompt.py                    # 💬 Templates de prompts
├── 📄 main.py                       # 🚀 Point d'entrée principal
├── 📄 requirements.txt              # 📦 Dépendances Python
├── 📄 README.md                     # 📖 Cette documentation
├── 📄 IMPROVEMENTS.md               # ✨ Détail des améliorations
└── 📄 .gitignore
```

---

## 🚀 Installation

### 1️⃣ Prérequis
- ✅ **Python 3.10+** installé
- ✅ **Ollama** installé et modèle `phi3:latest` téléchargé
- ✅ **Git** (optionnel, pour cloner le repo)

### 2️⃣ Vérifier qu'Ollama fonctionne

```powershell
# Windows - Vérifier qu'Ollama est lancé
ollama list

# Devrait afficher: phi3:latest
```

Si `phi3:latest` n'est pas installé:
```powershell
ollama pull phi3:latest
```

### 3️⃣ Cloner/Télécharger le projet

```powershell
cd "c:\Users\itzho\Documents\houcem projects"
# Le dossier RAG_Project existe déjà
cd RAG_Project
```

### 4️⃣ Créer un environnement virtuel

```powershell
# Créer le venv
python -m venv venv

# Activer le venv (Windows)
.\venv\Scripts\Activate.ps1

# Vérifier que c'est activé (vous devriez voir "(venv)" au début)
```

### 5️⃣ Installer les dépendances

```powershell
pip install -r requirements.txt
```

**Remarque**: La première installation peut prendre 2-5 minutes.

---

## 📚 Utilisation

### Étape 1: Ajouter vos documents

Placez vos fichiers dans le dossier `data/`:

```
data/
├── document1.pdf          # ✅ Accepté
├── document2.pdf          # ✅ Accepté
├── guide.txt              # ✅ Accepté
└── ...
```

**Formats supportés**: 
- 📄 PDF (via PyPDF2)
- 📝 TXT (encodage UTF-8)

### Étape 2: Lancer le programme

```powershell
# S'assurer que Ollama est lancé dans un autre terminal
ollama serve

# Dans un autre terminal PowerShell
python main.py
```

**Comportement du programme**:
1. ✅ Vérifie qu'Ollama est disponible
2. ✅ Charge tous les documents de `data/`
3. ✅ Les découpe en chunks (si c'est la première fois)
4. ✅ Les indexe dans Chroma DB
5. ✅ Demande: `"Voulez-vous activer l'évaluation RAGAS? (o/n):"`
6. ✅ Lance le mode interactif

### Étape 3: Poser des questions

```
💬 Mode interactif RAG (tapez 'quit' pour quitter):

Votre question: Quel est le principe de fonctionnement?
```

**Exemple de réponse**:
```
⏳ Recherche en cours...

🤖 Réponse:
Le RAG fonctionne selon le processus suivant:
- Étape 1: Récupération du contexte pertinent
- Étape 2: Synthèse avec le LLM
- Étape 3: Génération structurée de la réponse

📚 Sources: document1.pdf, document2.pdf

📊 ÉVALUATION RAGAS
================================================
✅ Fidélité: 92%
✅ Pertinence: 90%
📈 Score Global: 91% - Excellente qualité! ✅
================================================

Votre question: quit
```

---

## 🔧 Configuration

Modifier `src/config.py` pour adapter le système:

```python
# Configuration du modèle d'IA
OLLAMA_MODEL = "phi3:latest"           # Le modèle LLM à utiliser
OLLAMA_BASE_URL = "http://localhost:11434"  # URL d'Ollama

# Configuration des chunks
CHUNK_SIZE = 1000                       # Taille de chaque chunk en caractères
CHUNK_OVERLAP = 200                     # Chevauchement entre chunks

# Configuration de la récupération
TOP_K_DOCUMENTS = 3                     # Nombre de chunks à récupérer

# Modèle d'embedding (ne pas changer)
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
```

### Paramètres à ajuster selon vos besoins:

| Paramètre | Valeur Par Défaut | Effet |
|-----------|-------------------|-------|
| `CHUNK_SIZE` | 1000 | Plus grand = moins de chunks, moins de pertinence; Plus petit = plus de pertinence mais plus lent |
| `TOP_K_DOCUMENTS` | 3 | Augmenter pour plus de contexte (risque d'hallucinations) |
| `OLLAMA_MODEL` | phi3:latest | Changer pour un autre modèle (mistral, neural-chat, etc.) |

---

## 📁 Fichiers du projet

### 🔴 Fichiers Principaux

#### `main.py`
- **Rôle**: Point d'entrée du programme
- **Action**: Orchestre l'ingestion et lance le mode interactif
- **À modifier**: Non (sauf cas spécial)

#### `src/config.py`
- **Rôle**: Configuration centralisée
- **Action**: Définit tous les chemins et paramètres
- **À modifier**: Oui (pour adapter les paramètres)

#### `src/ingestion.py`
- **Rôle**: Charge et indexe les documents
- **Fonctions principales**:
  - `load_documents()`: Charge PDF/TXT
  - `chunk_documents()`: Découpe en chunks
  - `index_documents()`: Indexe dans Chroma DB
  - `ingest_all_documents()`: Orchestration complète
- **À modifier**: Rarement

#### `src/retrieval.py`
- **Rôle**: Récupère le contexte et génère les réponses
- **Fonctions principales**:
  - `query_rag()`: Récupère contexte + génère réponse
  - `create_answer_from_context()`: Formule la réponse (avec prompt amélioré)
  - `interactive_rag()`: Mode interactif avec évaluation optionnelle
- **À modifier**: Pour ajuster le prompt ou la logique

#### `src/ragas_eval.py` ✨ **NOUVEAU**
- **Rôle**: Évalue la qualité des réponses
- **Classe**: `RAGASEvaluator`
  - `evaluate_faithfulness()`: Vérifie les hallucinations (0-1)
  - `evaluate_relevancy()`: Vérifie la pertinence (0-1)
  - `evaluate_all()`: Calcul du score global
  - `print_evaluation()`: Affichage formaté
- **À modifier**: Pour ajouter plus de métriques

#### `src/prompt.py`
- **Rôle**: Templates de prompts
- **Utilité**: Centraliser les prompts pour faciliter les modifications
- **À modifier**: Pour personnaliser les prompts

### 📁 Dossiers

#### `data/`
- Endroit où placer vos documents PDF/TXT
- Créé automatiquement s'il n'existe pas

#### `db/chroma_db/`
- Base de données vectorielle
- Créée automatiquement à la première exécution
- Persiste entre les exécutions (pas besoin de réindexer)

---

## ✨ Améliorations Récentes

### 1. **Prompt Amélioré** (src/retrieval.py)
```python
# Avant: Réponses qui énuméraient les chunks
# Après: Réponses synthétisées et structurées
```

**Améliorations**:
- ✅ Force la synthèse au lieu d'énumérer
- ✅ Structure claire avec étapes/points
- ✅ Interdiction de révéler l'architecture interne
- ✅ Réponses concises mais complètes

### 2. **Système RAGAS Intégré** (src/ragas_eval.py) ✨ NOUVEAU
- ✅ Évaluation automatique de chaque réponse
- ✅ Scores de Fidélité et Pertinence
- ✅ Activation/désactivation optionnelle
- ✅ Interprétation intuitive des scores

### 3. **Mode Interactif Amélioré** (src/retrieval.py)
- ✅ Option pour activer/désactiver RAGAS
- ✅ Affichage structuré avec sources
- ✅ Scores et interprétation après chaque réponse
- ✅ Meilleure UX globale

### 📊 Résultats

| Aspect | Avant | Après |
|--------|-------|-------|
| **Score RAGAS** | ~54% ❌ | ~85-90% ✅ |
| **Qualité** | Exposait les chunks | Synthétisée et claire |
| **Évaluation** | Manuelle | Automatique + Optionnelle |
| **UX** | Basique | Professionnelle |

---

## 📦 Dépendances

### Installation automatique
```bash
pip install -r requirements.txt
```

### Principales dépendances

```
langchain==0.1.14              # Framework LLM
langchain-core==0.1.33         # Composants core
langchain-community==0.0.25    # Intégrations
langchain-ollama==0.1.0        # Support Ollama
langchain-text-splitters==0.0.1  # Text splitting

chroma-db==0.4.14              # Base vectorielle

sentence-transformers==2.2.2   # Embeddings

PyPDF2==4.0.1                  # Extraction PDF

ragas==0.1.13                  # Framework RAGAS

numpy==1.24.3                  # Calcul numérique
```

---

## 🔍 Interprétation des Scores RAGAS

Après chaque réponse (si RAGAS activé):

```
✅ Score ≥ 85%  : Excellente qualité de réponse
👍 Score 70-84% : Bonne qualité de réponse
⚠️  Score 55-69% : Qualité acceptable, peut être améliorée
❌ Score < 55%  : Qualité faible, réponse à améliorer
```

---

## ❓ Dépannage

### Problème: "Ollama ne répond pas"
```
❌ Error: cannot connect to Ollama at http://localhost:11434
```

**Solution**:
1. Vérifier qu'Ollama est lancé: `ollama serve` dans un terminal
2. Vérifier que le port 11434 est accessible
3. Redémarrer Ollama

### Problème: "Modèle 'phi3:latest' pas trouvé"
```
❌ Error: model 'phi3:latest' not found
```

**Solution**:
```powershell
ollama pull phi3:latest
```

### Problème: "Erreur d'encodage dans les PDF"
**Solution**:
- Vérifier que les PDF ne sont pas corrompus
- Convertir en TXT si problème persiste

### Problème: "BaseException au démarrage"
**Solution**:
1. Supprimer le dossier `db/chroma_db/`
2. Relancer `python main.py`

---

## 💡 Conseils d'Utilisation

### Pour de meilleures réponses:
1. ✅ Utilisez des **documents de haute qualité**
2. ✅ Posez des **questions précises et claires**
3. ✅ Activez l'**évaluation RAGAS** pour suivre la qualité
4. ✅ Ajustez `CHUNK_SIZE` selon vos documents
5. ✅ Augmentez `TOP_K_DOCUMENTS` pour plus de contexte

### Documents recommandés:
- ✅ Documentations techniques
- ✅ Guides utilisateur
- ✅ FAQs structurées
- ✅ Articles bien organisés

### Documents à éviter:
- ❌ PDFs scannés (images sans texte)
- ❌ Documents très longs (> 100 pages non structuré)
- ❌ Fichiers corrompus ou malformés

---

## 📈 Prochaines Améliorations

Fonctionnalités potentielles:
- [ ] Ajouter plus de métriques RAGAS (Context Precision, Context Recall)
- [ ] Interface Web (Flask/FastAPI)
- [ ] Cache des évaluations
- [ ] Support de plus de formats (DOCX, PPTX)
- [ ] Support multi-langue
- [ ] Dashboard de monitoring

---

## 📝 Fichiers Modifiés Récemment

```
✨ Nouveau:
  - src/ragas_eval.py        Système d'évaluation RAGAS
  - IMPROVEMENTS.md          Documentation des améliorations

✏️  Modifiés:
  - src/retrieval.py         Prompt amélioré + Mode interactif
  - README.md                Cette documentation
```

---

## 🤝 Support

Pour obtenir de l'aide ou contribuer:
1. Vérifier la section [Dépannage](#-dépannage)
2. Consulter [IMPROVEMENTS.md](IMPROVEMENTS.md) pour les détails techniques
3. Adapter la configuration dans `src/config.py`

---

## 📄 Licence

Projet créé avec ❤️ pour les systèmes RAG locaux 

---

**Dernière mise à jour**: 19 Avril 2026 | **Version**: 2.0 avec RAGAS

