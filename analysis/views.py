import os
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import re
import openai

# Use OpenRouter instead of OpenAI
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@csrf_exempt
def chatbot_analysis(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body)
        query = data.get("query", "").lower()

        # Load data
        file_path = os.path.join(BASE_DIR, 'analysis', 'data', 'Sample_data (1).xlsx')
        df = pd.read_excel(file_path)
        df['year'] = df['year'].astype(int)

        # Normalize area list
        area_list = [str(area).lower() for area in df['final location'].dropna().unique()]
        found_areas = [area for area in area_list if area in query]

        # Find year limit
        match = re.search(r"last (\d+) years", query)
        year_limit = int(match.group(1)) if match else None

        latest_year = df['year'].max()
        if year_limit:
            df = df[df['year'] >= (latest_year - year_limit + 1)]

        # 📌 Case 1: Compare two areas (for demand)
        if "compare" in query and len(found_areas) == 2:
            area1, area2 = found_areas
            data1 = df[df['final location'].str.lower() == area1].groupby('year')['total sold - igr'].sum()
            data2 = df[df['final location'].str.lower() == area2].groupby('year')['total sold - igr'].sum()
            years = sorted(list(set(data1.index).union(set(data2.index))))

            chart_data = []
            for year in years:
                chart_data.append({
                    "year": int(year),
                    area1.title(): int(data1.get(year, 0)),
                    area2.title(): int(data2.get(year, 0))
                })

            # 🔁 Generate LLM-based summary using merged comparison data
            merged_df = pd.DataFrame(chart_data)
            summary = generate_summary_openrouter(merged_df, f"{area1.title()} vs {area2.title()}", "demand comparison")

            return JsonResponse({
                "summary": summary,
                "chart": chart_data,
                "table": []  # Could optionally merge both tables too
            })

        # 📌 Case 2: Single area analysis (price or demand)
        if len(found_areas) == 1:
            area = found_areas[0]
            filtered = df[df['final location'].str.lower() == area]

            # Determine metric
            if "price" in query:
                metric_col = 'flat - weighted average rate'
            elif "demand" in query:
                metric_col = 'total sold - igr'
            else:
                metric_col = 'flat - weighted average rate'

            chart_data = filtered.groupby('year')[metric_col].mean().reset_index()
            chart_json = chart_data.rename(columns={metric_col: 'value'}).to_dict(orient='records')
            table_data = filtered.fillna("").to_dict(orient='records')

            metric_name = "price" if "price" in query else "flat rate"

            # 🔁 Replace with LLM summary
            summary = generate_summary_openrouter(filtered, area.title(), metric_name)

            return JsonResponse({
                "summary": summary,
                "chart": chart_json,
                "table": table_data
            })

        # 📌 No valid area found
        return JsonResponse({"summary": "Could not detect valid areas in your query.", "chart": [], "table": []})


    except Exception as e:
        import traceback
        print("💥 INTERNAL SERVER ERROR:")
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


def generate_summary_openrouter(df, area, metric):
    prompt = f"Give a short summary of the following real estate data for {area} showing {metric}:\n\n"
    prompt += str(df.head(5).to_dict(orient="records"))

    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct",  # ✅ Or try openai/gpt-3.5, anthropic/claude-2
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )

    return response['choices'][0]['message']['content'].strip()
