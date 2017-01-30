vector<int> PostorderTraversal(const unique_ptr<BinaryTreeNode<int>> &tree){
    if (tree == nullptr){
        return {};
    }

    stack<BinaryTreeNode<int>*> path;
    BinaryTreeNode<int> *prev = nullptr;
    path.emplace(tree.get());
    vector<int> postorder_sequence;
    while (!path.empty()){
        auto curr = path.top();
        if (prev == nullptr || prev->left.get() == curr || prev->right.get() == curr){
            if (curr->left != nullptr){
                path.emplace(curr->left.get());
            }
            else if (curr->right != nullptr){
                path.emplace(curr->right.get())
            }
            else {
                postorder_sequence.emplace_back(curr->data);
                path.pop();
            }
        }
        else if (curr->left.get() == prev){
            if (curr->right != nullptr){
                path.emplace(curr->right.get())
            }
            else {
                postorder_sequence.emplace_back(curr->data);
                path.pop();
            }
        }
        else {
            postorder_sequence.emplace_back(curr->data);
            path.pop();
        }
        prev = curr;
    }
    return postorder_sequence;
}
