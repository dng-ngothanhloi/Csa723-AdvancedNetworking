#!/bin/bash

# Script test cho create_issues.sh
# Usage: ./test_create_issues.sh

echo "=== Test Script for create_issues.sh ==="
echo

# Test 1: Kiểm tra script tồn tại
echo "Test 1: Kiểm tra script tồn tại"
if [ -f "create_issues.sh" ]; then
    echo "✓ Script create_issues.sh tồn tại"
else
    echo "✗ Script create_issues.sh không tồn tại"
    exit 1
fi
echo

# Test 2: Kiểm tra quyền thực thi
echo "Test 2: Kiểm tra quyền thực thi"
if [ -x "create_issues.sh" ]; then
    echo "✓ Script có quyền thực thi"
else
    echo "✗ Script không có quyền thực thi"
    echo "Chạy: chmod +x create_issues.sh"
fi
echo

# Test 3: Kiểm tra file input tồn tại
echo "Test 3: Kiểm tra file input"
if [ -f "Tasklist-NOMA.md" ]; then
    echo "✓ File Tasklist-NOMA.md tồn tại"
else
    echo "✗ File Tasklist-NOMA.md không tồn tại"
fi
echo

# Test 4: Kiểm tra GitHub CLI
echo "Test 4: Kiểm tra GitHub CLI"
if command -v gh &> /dev/null; then
    echo "✓ GitHub CLI đã cài đặt"
    
    # Kiểm tra đăng nhập
    if gh auth status &> /dev/null; then
        echo "✓ Đã đăng nhập GitHub CLI"
    else
        echo "✗ Chưa đăng nhập GitHub CLI"
        echo "Chạy: gh auth login"
    fi
else
    echo "✗ GitHub CLI chưa cài đặt"
    echo "Cài đặt: https://cli.github.com/"
fi
echo

# Test 5: Test parsing file (dry run)
echo "Test 5: Test parsing file (dry run)"
echo "Đọc file Tasklist-NOMA.md và đếm số task..."

task_count=0
while IFS= read -r line; do
    if [[ $line =~ ^##[[:space:]]+[0-9]+\.[[:space:]]+(.+)$ ]]; then
        task_count=$((task_count + 1))
        echo "  Task $task_count: ${BASH_REMATCH[1]}"
    fi
done < "Tasklist-NOMA.md"

echo "✓ Tìm thấy $task_count task trong file"
echo

# Test 6: Hiển thị template sẽ được sử dụng
echo "Test 6: Template selection"
filename="Tasklist-NOMA.md"
case "$filename" in
    Tasklist-*.md)
        template="task-request"
        ;;
    Featurelist-*.md|RequirementList-*.md|FunctionList-*.md)
        template="feature_request"
        ;;
    Feedbacklist-*.md|BugList-*.md|IssueList-*.md)
        template="bug_report"
        ;;
    *)
        template="task-request"
        ;;
esac
echo "✓ File $filename sẽ sử dụng template: $template"
echo

# Test 7: Kiểm tra template files
echo "Test 7: Kiểm tra template files"
templates=("task-request" "feature_request" "bug_report")
for template in "${templates[@]}"; do
    if [ -f ".github/ISSUE_TEMPLATE/${template}.md" ]; then
        echo "✓ Template ${template}.md tồn tại"
    else
        echo "✗ Template ${template}.md không tồn tại"
    fi
done
echo

# Test 8: Demo command
echo "Test 8: Demo command"
echo "Để tạo issues từ Tasklist-NOMA.md, chạy:"
echo "  ./create_issues.sh Tasklist-NOMA.md dng-ngothanhloi/isa701-csdl"
echo
echo "Hoặc với repository mặc định:"
echo "  ./create_issues.sh Tasklist-NOMA.md"
echo

echo "=== Test hoàn thành ==="
echo "Nếu tất cả test đều pass (✓), bạn có thể chạy script để tạo issues."
echo "Nếu có test fail (✗), hãy khắc phục trước khi chạy script." 