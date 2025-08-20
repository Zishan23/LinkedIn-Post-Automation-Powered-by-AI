#!/usr/bin/env python3
"""
LIME & SHAP Analysis for LinkedIn Post Automation

This script analyzes AI-generated LinkedIn posts using LIME and SHAP to understand:
- Which words/phrases contribute most to sentiment scores
- How different demographic prompts affect content generation
- Potential biases in the AI-generated content
"""

import os
import sys
import requests
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# Add server directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'server'))

try:
    import lime
    from lime.lime_text import LimeTextExplainer
    print("✅ LIME: Available")
except ImportError:
    print("❌ LIME: Not available")
    lime = None

try:
    import shap
    print("✅ SHAP: Available")
except ImportError:
    print("❌ SHAP: Not available")
    shap = None

# Configuration
BACKEND_URL = "http://localhost:5005"

def test_content_generation():
    """Test if content generation is working"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/v1/generate-content",
            json={"query": "Write a professional LinkedIn post about leadership"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            content = data.get('content', '')
            print(f"Generated content: {content[:100]}...")
            return True, content
        else:
            print(f"❌ Content generation failed: {response.status_code}")
            return False, ""
    except Exception as e:
        print(f"❌ Error testing content generation: {e}")
        return False, ""

def generate_demographic_content():
    """Generate content for different demographic variants"""
    categories = {
        'Gender': ['male', 'female', 'non-binary'],
        'Experience Level': ['entry-level', 'mid-career', 'senior'],
        'Industry': ['technology', 'healthcare', 'finance']
    }
    
    prompts = {
        'Gender': {
            'male': "Write a LinkedIn post about professional development from a male perspective",
            'female': "Write a LinkedIn post about professional development from a female perspective", 
            'non-binary': "Write a LinkedIn post about professional development from a professional perspective"
        },
        'Experience Level': {
            'entry-level': "Write a LinkedIn post about starting your career journey",
            'mid-career': "Write a LinkedIn post about advancing in your career",
            'senior': "Write a LinkedIn post about leadership and mentoring"
        },
        'Industry': {
            'technology': "Write a LinkedIn post about innovation in technology",
            'healthcare': "Write a LinkedIn post about healthcare advancements",
            'finance': "Write a LinkedIn post about financial planning and growth"
        }
    }
    
    content_samples = []
    
    print("🚀 Generating content for bias analysis...")
    for category, variants in tqdm(categories.items(), desc="Categories"):
        for variant in variants:
            try:
                prompt = prompts[category][variant]
                response = requests.post(
                    f"{BACKEND_URL}/api/v1/generate-content",
                    json={"query": prompt},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    content = data.get('content', '')
                    
                    content_samples.append({
                        'category': category,
                        'variant': variant,
                        'content': content,
                        'word_count': len(content.split()),
                        'prompt': prompt
                    })
                    
                    print(f"✅ Generated {category}: {variant}")
                else:
                    print(f"❌ Failed to generate {category}: {variant}")
                    
            except Exception as e:
                print(f"❌ Error generating {category}: {variant} - {e}")
    
    return content_samples

def simple_sentiment_analysis(text):
    """Simple rule-based sentiment analysis"""
    positive_words = ['success', 'growth', 'opportunity', 'innovation', 'leadership', 'excellent', 'amazing', 'great', 'wonderful', 'inspiring']
    negative_words = ['challenge', 'difficulty', 'problem', 'failure', 'struggle', 'terrible', 'awful', 'horrible', 'disappointing']
    
    text_lower = text.lower()
    pos_score = sum(1 for word in positive_words if word in text_lower)
    neg_score = sum(1 for word in negative_words if word in text_lower)
    
    if pos_score > neg_score:
        return "positive"
    elif neg_score > pos_score:
        return "negative"
    else:
        return "neutral"

def analyze_sentiment_batch(content_samples):
    """Analyze sentiment for all content samples"""
    print("🔍 Analyzing sentiment for all samples...")
    
    for sample in tqdm(content_samples, desc="Sentiment Analysis"):
        try:
            sentiment = simple_sentiment_analysis(sample['content'])
            sample['sentiment'] = sentiment
        except Exception as e:
            print(f"❌ Error analyzing sample: {e}")
            sample['sentiment'] = 'neutral'
    
    print(f"✅ Analyzed {len(content_samples)} samples")
    return content_samples

def setup_lime_explainer():
    """Set up LIME explainer for text analysis"""
    try:
        if lime is None:
            print("❌ LIME not available")
            return None
        
        explainer = LimeTextExplainer(class_names=['negative', 'neutral', 'positive'])
        print("✅ LIME explainer ready!")
        return explainer
    except Exception as e:
        print(f"❌ Error setting up LIME: {e}")
        return None

def perform_lime_analysis(content_samples, lime_explainer):
    """Perform LIME analysis on content samples"""
    if lime_explainer is None:
        print("⚠️  Skipping LIME analysis")
        return []
    
    print("🔍 Performing LIME analysis...")
    
    lime_results = []
    for sample in tqdm(content_samples, desc="LIME Analysis"):
        try:
            # Create a simple classifier function for LIME
            def classifier_fn(texts):
                # Simple rule-based classification for demonstration
                results = []
                for text in texts:
                    positive_words = ['success', 'growth', 'opportunity', 'innovation', 'leadership']
                    negative_words = ['challenge', 'difficulty', 'problem', 'failure', 'struggle']
                    
                    text_lower = text.lower()
                    pos_score = sum(1 for word in positive_words if word in text_lower)
                    neg_score = sum(1 for word in negative_words if word in text_lower)
                    
                    if pos_score > neg_score:
                        results.append(2)  # positive
                    elif neg_score > pos_score:
                        results.append(0)  # negative
                    else:
                        results.append(1)  # neutral
                
                return np.array(results)
            
            # Explain the sample
            exp = lime_explainer.explain_instance(
                sample['content'], 
                classifier_fn, 
                num_features=10,
                num_samples=100
            )
            
            lime_results.append({
                'category': sample['category'],
                'variant': sample['variant'],
                'explanation': exp,
                'content': sample['content']
            })
            
        except Exception as e:
            print(f"❌ Error in LIME analysis for {sample['category']}: {sample['variant']} - {e}")
    
    print(f"✅ LIME analysis completed for {len(lime_results)} samples")
    return lime_results

def setup_shap_analysis():
    """Set up SHAP analysis"""
    try:
        if shap is None:
            print("❌ SHAP not available")
            return None
        
        print("✅ SHAP explainer ready!")
        return True
    except Exception as e:
        print(f"❌ Error setting up SHAP: {e}")
        return None

def perform_shap_analysis(content_samples, shap_explainer):
    """Perform SHAP analysis on content samples"""
    if shap_explainer is None:
        print("⚠️  Skipping SHAP analysis")
        return [], []
    
    print("🔍 Computing SHAP values...")
    
    try:
        # Create a simple feature matrix for SHAP
        # Extract basic text features
        features = []
        texts = []
        
        for sample in content_samples:
            text = sample['content']
            texts.append(text)
            
            # Simple feature extraction
            feature_vector = [
                len(text.split()),  # word count
                len(text),  # character count
                text.count('!'),  # exclamation marks
                text.count('?'),  # question marks
                text.count('#'),  # hashtags
                text.count('@'),  # mentions
                text.count('http'),  # links
                sum(1 for c in text if c.isupper()),  # uppercase letters
                sum(1 for c in text if c.isdigit()),  # digits
                len([w for w in text.split() if len(w) > 6])  # long words
            ]
            features.append(feature_vector)
        
        feature_matrix = np.array(features)
        
        # Create a simple model for SHAP
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.preprocessing import LabelEncoder
        
        # Encode categories for classification
        le = LabelEncoder()
        categories_encoded = le.fit_transform([s['category'] for s in content_samples])
        
        # Train a simple classifier
        clf = RandomForestClassifier(n_estimators=10, random_state=42)
        clf.fit(feature_matrix, categories_encoded)
        
        # Create SHAP explainer
        explainer = shap.TreeExplainer(clf)
        shap_values = explainer.shap_values(feature_matrix)
        
        print(f"✅ SHAP analysis completed for {len(texts)} samples")
        return shap_values, texts
        
    except Exception as e:
        print(f"❌ Error in SHAP analysis: {e}")
        return [], []

def create_visualizations(content_samples, lime_results, shap_values, shap_texts):
    """Create comprehensive visualizations"""
    print("🎨 Creating visualizations...")
    
    # Set style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 15))
    
    # 1. Content Distribution by Category
    ax1 = plt.subplot(3, 3, 1)
    category_counts = pd.DataFrame(content_samples).groupby('category').size()
    category_counts.plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_title('Content Distribution by Category', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Number of Samples')
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Word Count Distribution
    ax2 = plt.subplot(3, 3, 2)
    word_counts = [s['word_count'] for s in content_samples]
    ax2.hist(word_counts, bins=15, color='lightgreen', alpha=0.7, edgecolor='black')
    ax2.set_title('Word Count Distribution', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Word Count')
    ax2.set_ylabel('Frequency')
    
    # 3. Sentiment Distribution
    ax3 = plt.subplot(3, 3, 3)
    if 'sentiment' in content_samples[0]:
        sentiment_counts = pd.DataFrame(content_samples).groupby('sentiment').size()
        sentiment_counts.plot(kind='pie', ax=ax3, autopct='%1.1f%%', colors=['#ff9999', '#66b3ff', '#99ff99'])
        ax3.set_title('Sentiment Distribution', fontsize=14, fontweight='bold')
    else:
        ax3.text(0.5, 0.5, 'No sentiment data', ha='center', va='center', transform=ax3.transAxes)
        ax3.set_title('Sentiment Distribution', fontsize=14, fontweight='bold')
    
    # 4. Category vs Word Count
    ax4 = plt.subplot(3, 3, 4)
    df = pd.DataFrame(content_samples)
    sns.boxplot(data=df, x='category', y='word_count', ax=ax4, palette='Set3')
    ax4.set_title('Word Count by Category', fontsize=14, fontweight='bold')
    ax4.set_ylabel('Word Count')
    ax4.tick_params(axis='x', rotation=45)
    
    # 5. Variant Analysis
    ax5 = plt.subplot(3, 3, 5)
    variant_counts = df.groupby(['category', 'variant']).size().unstack(fill_value=0)
    variant_counts.plot(kind='bar', ax=ax5, stacked=True, colormap='tab20')
    ax5.set_title('Content Distribution by Variant', fontsize=14, fontweight='bold')
    ax5.set_ylabel('Number of Samples')
    ax5.tick_params(axis='x', rotation=45)
    ax5.legend(title='Variant', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 6. Content Length Analysis
    ax6 = plt.subplot(3, 3, 6)
    df['char_count'] = df['content'].str.len()
    sns.scatterplot(data=df, x='word_count', y='char_count', hue='category', ax=ax6, s=100)
    ax6.set_title('Word Count vs Character Count', fontsize=14, fontweight='bold')
    ax6.set_xlabel('Word Count')
    ax6.set_ylabel('Character Count')
    
    # 7. SHAP Summary Plot (if available)
    ax7 = plt.subplot(3, 3, 7)
    if len(shap_values) > 0:
        try:
            # For tree-based models, shap_values is a list
            if isinstance(shap_values, list):
                shap_values_array = shap_values[0] if len(shap_values) > 0 else shap_values
            else:
                shap_values_array = shap_values
            
            # Create feature names
            feature_names = [
                'Word Count', 'Char Count', 'Exclamations', 'Questions', 
                'Hashtags', 'Mentions', 'Links', 'Uppercase', 'Digits', 'Long Words'
            ]
            
            # Plot SHAP summary
            shap.summary_plot(shap_values_array, feature_matrix, feature_names=feature_names, 
                            show=False, plot_type="bar", ax=ax7)
            ax7.set_title('SHAP Feature Importance', fontsize=14, fontweight='bold')
        except Exception as e:
            ax7.text(0.5, 0.5, f'SHAP Error:\n{str(e)[:50]}', ha='center', va='center', transform=ax7.transAxes)
            ax7.set_title('SHAP Feature Importance', fontsize=14, fontweight='bold')
    else:
        ax7.text(0.5, 0.5, 'No SHAP data', ha='center', va='center', transform=ax7.transAxes)
        ax7.set_title('SHAP Feature Importance', fontsize=14, fontweight='bold')
    
    # 8. LIME Results Summary (if available)
    ax8 = plt.subplot(3, 3, 8)
    if lime_results:
        try:
            # Count explanations by category
            lime_category_counts = {}
            for result in lime_results:
                cat = result['category']
                lime_category_counts[cat] = lime_category_counts.get(cat, 0) + 1
            
            categories = list(lime_category_counts.keys())
            counts = list(lime_category_counts.values())
            
            ax8.bar(categories, counts, color='orange', alpha=0.7)
            ax8.set_title('LIME Analysis Coverage', fontsize=14, fontweight='bold')
            ax8.set_ylabel('Number of Explanations')
            ax8.tick_params(axis='x', rotation=45)
        except Exception as e:
            ax7.text(0.5, 0.5, f'LIME Error:\n{str(e)[:50]}', ha='center', va='center', transform=ax7.transAxes)
            ax7.set_title('LIME Analysis Coverage', fontsize=14, fontweight='bold')
    else:
        ax8.text(0.5, 0.5, 'No LIME data', ha='center', va='center', transform=ax8.transAxes)
        ax8.set_title('LIME Analysis Coverage', fontsize=14, fontweight='bold')
    
    # 9. Overall Statistics
    ax9 = plt.subplot(3, 3, 9)
    ax9.axis('off')
    
    # Calculate statistics
    total_samples = len(content_samples)
    avg_word_count = np.mean([s['word_count'] for s in content_samples])
    categories_covered = len(set(s['category'] for s in content_samples))
    
    stats_text = f"""
    📊 ANALYSIS SUMMARY
    
    Total Samples: {total_samples}
    Categories: {categories_covered}
    Avg Word Count: {avg_word_count:.1f}
    
    🔍 Analysis Status:
    • Content Generation: ✅
    • Sentiment Analysis: {'✅' if 'sentiment' in content_samples[0] else '❌'}
    • LIME Analysis: {'✅' if lime_results else '❌'}
    • SHAP Analysis: {'✅' if len(shap_values) > 0 else '❌'}
    
    📈 Key Insights:
    • Content varies across {categories_covered} categories
    • Average post length: {avg_word_count:.1f} words
    • Ready for bias detection analysis
    """
    
    ax9.text(0.05, 0.95, stats_text, transform=ax9.transAxes, fontsize=10, 
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
    
    plt.tight_layout()
    
    # Save the plot
    output_path = "lime_shap_analysis_results.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Visualization saved as: {output_path}")
    
    # Show the plot
    plt.show()
    
    return output_path

def main():
    """Main analysis function"""
    print("🚀 Starting LIME & SHAP Analysis for LinkedIn Post Automation")
    print("=" * 60)
    
    # Setup
    print("🔧 Setting up analysis environment...")
    print(f"🔗 Backend URL: {BACKEND_URL}")
    
    # Check package availability
    print("📦 Package Status:")
    print(f"  LIME: {'✅ Available' if lime else '❌ Not available'}")
    print(f"  SHAP: {'✅ Available' if shap else '❌ Not available'}")
    
    # Test content generation
    print("🧪 Testing content generation...")
    content_working, test_content = test_content_generation()
    print(f"✅ Content generation working: {content_working}")
    
    if not content_working:
        print("❌ Cannot proceed without content generation")
        return
    
    # Generate demographic content
    print("📊 Defining demographic variants...")
    content_samples = generate_demographic_content()
    
    if not content_samples:
        print("❌ No content samples generated")
        return
    
    print(f"✅ Generated {len(content_samples)} content samples")
    
    # Analyze content samples
    print("\n📊 Content Samples Overview:")
    print(f"Total samples: {len(content_samples)}")
    categories = list(set(s['category'] for s in content_samples))
    print(f"Categories: {categories}")
    
    df = pd.DataFrame(content_samples)
    print(f"Average word count: {df['word_count'].mean():.1f}")
    
    # Analyze sentiment
    print("\n🔍 Analyzing sentiment for all samples...")
    content_samples = analyze_sentiment_batch(content_samples)
    
    # Setup LIME
    print("\n🔍 Setting up LIME explainer...")
    lime_explainer = setup_lime_explainer()
    
    # Perform LIME analysis
    print("\n🔍 Performing LIME analysis...")
    lime_results = perform_lime_analysis(content_samples, lime_explainer)
    
    # Setup SHAP
    print("\n🔍 Setting up SHAP analysis...")
    shap_explainer = setup_shap_analysis()
    
    # Perform SHAP analysis
    print("\n🔍 Computing SHAP values...")
    shap_values, shap_texts = perform_shap_analysis(content_samples, shap_explainer)
    
    # Create visualizations
    print("\n🎨 Creating comprehensive visualizations...")
    output_path = create_visualizations(content_samples, lime_results, shap_values, shap_texts)
    
    print(f"\n🎉 Analysis Complete!")
    print(f"📊 Results saved to: {output_path}")
    print(f"📈 Generated {len(content_samples)} content samples")
    print(f"🔍 LIME explanations: {len(lime_results)}")
    print(f"📊 SHAP values computed: {len(shap_values) > 0}")
    
    # Save data to CSV for further analysis
    df = pd.DataFrame(content_samples)
    csv_path = "content_analysis_data.csv"
    df.to_csv(csv_path, index=False)
    print(f"💾 Data saved to: {csv_path}")

if __name__ == "__main__":
    main() 