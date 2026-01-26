// ===============================================
// メインの処理：ページのDOMが読み込まれたら実行
// ===============================================
document.addEventListener('DOMContentLoaded', () => {
    // 1. 共通パーツ（ヘッダー・フッター）を読み込む
    loadCommonParts();

    // 2. ハンバーガーメニューを初期化する
    //    (ヘッダーが静的なページでも動くように、ここでも呼び出す)
    initHamburgerMenu();

    // 3. テンプレート一覧ページで、カテゴリの絞り込み表示を処理する
    handleCategoryFilter();
});


// ===============================================
// 共通パーツ（ヘッダー・フッター）を読み込む関数
// ===============================================
function loadCommonParts() {
    // ヘッダーの読み込み
    const headerPlaceholder = document.getElementById('header-placeholder');
    if (headerPlaceholder) {
        fetch('_header.html')
            .then(response => response.text())
            .then(data => {
                headerPlaceholder.innerHTML = data;
                // ★重要：ヘッダーが読み込まれた後に、ハンバーガーメニューを初期化
                initHamburgerMenu(); 
            });
    }

    // フッターの読み込み
    const footerPlaceholder = document.getElementById('footer-placeholder');
    if (footerPlaceholder) {
        fetch('_footer.html')
            .then(response => response.text())
            .then(data => {
                footerPlaceholder.innerHTML = data;
            });
    }
}


// ===============================================
// ハンバーガーメニューを初期化する関数
// ===============================================
function initHamburgerMenu() {
    const hamburgerMenu = document.getElementById('hamburger-menu');
    const navMenu = document.getElementById('nav-menu');

    // 要素が見つからない場合は、何もしない（エラーを防ぐ）
    if (!hamburgerMenu || !navMenu) {
        return;
    }

    hamburgerMenu.addEventListener('click', () => {
        hamburgerMenu.classList.toggle('is-active');
        navMenu.classList.toggle('is-active');
    });
}


// ===============================================
// テンプレート一覧ページで、カテゴリを有効化する関数
// ===============================================
function handleCategoryFilter() {
    // 現在のページが template-list.html の場合のみ、この処理を実行
    if (!window.location.pathname.includes('template-list.html')) {
        return;
    }
        
    // URLから 'category' パラメータを取得
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get('category');

    // categoryパラメータが存在しない場合は、何もしない
    if (!category) {
        return;
    }

    // サイドバーのすべてのリンクを取得
    const sidebarLinks = document.querySelectorAll('.sidebar a');
    if (sidebarLinks.length === 0) {
        return;
    }

    let categoryFound = false;
    sidebarLinks.forEach(link => {
        // まず、すべてのリンクから 'active' クラスを一旦削除
        link.classList.remove('active');

        // リンクの data-category の値がURLのパラメータと一致したら
        if (link.dataset.category === category) {
            // そのリンクに 'active' クラスを追加
            link.classList.add('active');
            categoryFound = true;
        }
    });

    // もしURLのカテゴリに一致するリンクがなかった場合（念のため）、
    // デフォルトの「すべて」をアクティブに戻す
    if (!categoryFound) {
        const allLink = document.querySelector('.sidebar a[data-category="all"]');
        if (allLink) {
            allLink.classList.add('active');
        }
    }
}
