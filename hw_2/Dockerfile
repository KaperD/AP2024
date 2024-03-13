FROM python:3 AS generate-tex
WORKDIR /ap/build
RUN pip install -i https://test.pypi.org/simple/ AP2024
COPY 2-solution.py .
RUN mkdir artifacts
RUN python 2-solution.py

FROM texlive/texlive:latest AS build-pdf
WORKDIR /tex/build
COPY --from=generate-tex /ap/build/artifacts/2-RESULT.tex .
COPY artifacts/mesh.png ./universe.jpg
RUN pdflatex 2-RESULT.tex
ENTRYPOINT ["cp", "2-RESULT.pdf", "/output/3-RESULT.pdf"]

# run with: docker run --rm -v $(pwd)/artifacts:/output $(docker build -q .)
