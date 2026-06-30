import streamlit as st


def calculate_accuracy(correct, attempted):
    if attempted == 0:
        return 0
    return (correct / attempted) * 100


def calculate_grade(accuracy):
    if accuracy >= 80:
        return "A"
    elif accuracy >= 60:
        return "B"
    elif accuracy >= 40:
        return "C"
    else:
        return "Needs Improvement"


def show_performance_report(name, subject, accuracy, grade):
    st.subheader("📊 Performance Report")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("👤 Student", name)
        st.metric("📚 Subject", subject)

    with col2:
        st.metric("🎯 Accuracy", f"{accuracy:.2f}%")
        st.metric("🎓 Grade", grade)


def show_analytics_dashboard(correct, wrong, skipped):
    st.subheader("📊 Analytics Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("✅ Correct", correct)

    with col2:
        st.metric("❌ Wrong", wrong)

    with col3:
        st.metric("⏭️ Skipped", skipped)

    chart_data = {
        "Correct": correct,
        "Wrong": wrong,
        "Skipped": skipped
    }

    st.bar_chart(chart_data)