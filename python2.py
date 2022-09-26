
      run: echo ::set-output name=modified::$(if git diff-index --quiet HEAD --; then echo "tidak"; else echo "ya"; fi)
    - name: Push perubahan
      if: steps.git-check.outputs.modified == 'ya' && github.event_name == 'push'
      run: |
        git config --global user.name 'bellshadebot'
        git config --global user.email 'bellshade07@gmail.com'
        git remote set-url origin https://x-access-token:${{ secrets.GITHUB_TOKEN }}@github.com/${{ github.repository }}
        git pull
        git commit -am "style: format otomatis dengan black dan isort"
        git push
      # test python dengan menggunakan pytest dengan perintah lanjutan
      # yaitu document testing
    - name: Test Python
      run: |
        echo "Mulai Jalankan testing docstring"
        pytest . --doctest-modules --ignore=Basic/ --cov-report=term-missing:skip-covered
      # test lint python jika black gagal reformat kode
    - name: Test Lint Python
      run: |
        echo "Mulai Jalankan testing flake8"
        flake8 .
      # mypy adalah unit testing diluar dari official python
      # yang berfungsi jika mengecek kode apakah terdapat kode
      # yang bersifat tidak berguna, terlalu rumit, atau kesalahan import

    - name: Test mypy
      run: mypy --ignore-missing-imports --install-types --non-interactive .
      # FIXME : kendala error beberapa directory mypy
      # mulai test coverage dan menampilkan hasil presentasi scanning dari pytest
    - name: Test coverage
      run: |
        echo "Mulai testing coverage"
        coverage run --source . -m pytest --doctest-modules --ignore=Basic/
      # membuat report untuk upload ke codecoverage

    #  kendala server github tidak respon pada coverage
    #  untuk sementara dinonaktifkan
    # - name: Hasil coverage
    #   run: |
    #     echo "Laporan coverage"
    #     coverage report -m
