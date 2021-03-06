# (())は算術を表す。0を偽と判定できる。commands[gh]があるか調べ、+であれば1 なければ0を出力
# [ ] による式と違って、値が0の時に偽値となる
if (( $+commands[gh] )); then
    function github_issue_open_browser() {
        local issue_id=$(gh issue list | fzf | awk '{print $1}' )
        if [ -n "$issue_id" ]; then
            gh issue view -w ${issue_id}
        fi
        zle redisplay
    }
fi
zle -N github_issue_open_browser
bindkey "^g^b^i" github_issue_open_browser
